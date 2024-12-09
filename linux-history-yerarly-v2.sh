#!/bin/bash
# The following line uses curl to reproducibly install and run the specified revision of torte.
# Alternatively, torte can be installed manually (see https://github.com/ekuiter/torte).
# In that case, make sure to check out the correct revision manually and run ./torte.sh <this-file>.
TORTE_REVISION=main; [[ $TOOL != torte ]] && builtin source <(curl -fsSL https://raw.githubusercontent.com/ekuiter/torte/$TORTE_REVISION/torte.sh) "$@"

# This experiment extracts a yearly history of feature models from the Linux kernel (x86).
SOLVE_TIMEOUT=1200

experiment-subjects() {
    add-linux-system
    add-linux-kconfig-revisions --revisions "$(echo "v2.5.45 v2.5.54 v2.6.1 v2.6.11 v2.6.15 v2.6.20 v2.6.24 v2.6.29 v2.6.33 v2.6.37 v3.2 v3.8 v3.13 v3.19 v4.4 v4.10 v4.15 v5.0 v5.5 v5.11 v5.16 v6.2 v6.7" | tr ' ' '\n')" --architecture "x86"
}

experiment-stages() {
    clone-systems
    tag-linux-revisions
    read-linux-names
    read-linux-architectures
    read-linux-configs
    read-statistics
    join-into read-statistics read-linux-names
    join-into read-statistics read-linux-architectures
    extract-kconfig-models
    join-into read-statistics kconfig
    transform-models-with-featjar --transformer model_to_smt_z3 --output-extension smt
    
    run \
        --stage dimacs \
        --image z3 \
        --input-directory model_to_smt_z3 \
        --command transform-into-dimacs-with-z3 \
        --jobs 16
    join-into model_to_smt_z3 dimacs
    join-into kconfig dimacs

    solve \
        --iterations 5 \
        --kind model-satisfiable \
        --timeout "$SOLVE_TIMEOUT" \
        --attempt-grouper "$(to-lambda linux-attempt-grouper)" \
        --solver_specs \
        sat-competition/02-zchaff,solver,satisfiable \
        sat-competition/03-Forklift,solver,satisfiable \
        sat-competition/04-zchaff,solver,satisfiable \
        sat-competition/05-SatELiteGTI.sh,solver,satisfiable \
        sat-competition/06-MiniSat,solver,satisfiable \
        sat-competition/07-RSat.sh,solver,satisfiable \
        sat-competition/08-MiniSat,solver,satisfiable \
        sat-competition/09-precosat,solver,satisfiable \
        sat-competition/10-CryptoMiniSat,solver,satisfiable \
        sat-competition/11-glucose.sh,solver,satisfiable \
        sat-competition/12-glucose.sh,solver,satisfiable \
        sat-competition/13-lingeling-aqw,solver,satisfiable \
        sat-competition/14-lingeling-ayv,solver,satisfiable \
        sat-competition/15-abcdSAT,solver,satisfiable \
        sat-competition/16-MapleCOMSPS_DRUP,solver,satisfiable \
        sat-competition/17-Maple_LCM_Dist,solver,satisfiable \
        sat-competition/18-MapleLCMDistChronoBT,solver,satisfiable \
        sat-competition/19-MapleLCMDiscChronoBT-DL-v3,solver,satisfiable \
        sat-competition/20-Kissat-sc2020-sat,solver,satisfiable \
        sat-competition/21-Kissat_MAB,solver,satisfiable \
        sat-competition/22-kissat_MAB-HyWalk,solver,satisfiable \
        sat-competition/23-sbva_cadical.sh,solver,satisfiable

}
          

# can be executed from output directory to copy and rename model files
copy-models() {
    mkdir -p models
    for f in kconfig/linux/*.model; do
        local revision
        revision=$(echo "$f" | cut -d/ -f3 | cut -d'[' -f1)
        cp "$f" "models/$(grep -E "^$revision," < read-statistics/output.csv | cut -d, -f3).model"
    done
}
