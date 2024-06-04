import pandas as pd
import argparse

def convert(name: str):
    columns = ["Dataname", "lin_pearson_corr", "expo_pearson_corr", "best-fittest"]
    df = pd.read_csv(name, usecols=columns)
    df.to_latex(name.replace(".csv",".tex"),index=False)

def main():
    parser = argparse.ArgumentParser(description="Convert a CSV file to LaTeX format.")
    parser.add_argument("name", type=str, help="The name of the CSV file to convert")
    
    args = parser.parse_args()
    convert(args.name)

if __name__ == "__main__":
    main()
