import pandas as pd
import argparse

def convert(name: str, suffix: str):
    columns = ["Dataname", "lin_pearson_corr", "expo_pearson_corr", "best-fittest"]
    df = pd.read_csv(name, usecols=columns)
    
    # Filter the DataFrame
    if suffix == "kconfigreader":
        filtered_df = df[~df["Dataname"].str.endswith("kmax-median.csv")]
    else:
        filtered_df = df[~df["Dataname"].str.endswith("kconfigreader-median.csv")]

    output_name = f"{name.replace('.csv', '')}-{suffix}.tex"
    filtered_df.to_latex(output_name, index=False)

def main():
    parser = argparse.ArgumentParser(description="Convert a CSV file to LaTeX format.")
    parser.add_argument("name", type=str, help="The name of the CSV file to convert")
    
    args = parser.parse_args()
    convert(args.name, "kconfigreader")
    convert(args.name, "kmax")

if __name__ == "__main__":
    main()
