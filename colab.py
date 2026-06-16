import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def clean_and_report(file_path):
    # 1. Read file
    print(f"Reading file: {file_path}")
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    else:
        print("Error: Use.csv or.xlsx file")
        return
    
    print(f"\n=== 1. RAW DATA INFO ===")
    print(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print("\nFirst 5 rows:")
    print(df.head())
    
    # 2. Data Cleaning Report
    print(f"\n=== 2. DATA CLEANING REPORT ===")
    
    # Missing values
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if len(missing_cols) > 0:
        print("\nMissing Values Found:")
        print(missing_cols)
    else:
        print("\nNo missing values found")
    
    # Duplicates
    duplicates = df.duplicated().sum()
    print(f"\nDuplicate Rows: {duplicates}")
    
    # 3. Clean data
    print(f"\n=== 3. CLEANING DATA ===")
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates()
    df_clean = df_clean.ffill().bfill() # fill missing values
    
    print(f"Removed {duplicates} duplicates")
    print(f"Filled missing values using forward/backward fill")
    print(f"Cleaned shape: {df_clean.shape[0]} rows, {df_clean.shape[1]} columns")
    
    # 4. Automated Visual Summary
    print(f"\n=== 4. SUMMARY STATISTICS ===")
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        print("\nNumeric Column Stats:")
        print(df_clean[numeric_cols].describe())
        
        # Generate plots
        for col in numeric_cols[:3]: # Plot first 3 numeric cols
            plt.figure(figsize=(8, 4))
            df_clean[col].hist(bins=20)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plt.savefig(f"hist_{col}.png")
            print(f"Saved plot: hist_{col}.png")
    else:
        print("No numeric columns found for visualization")
    
    # 5. Export cleaned data
    output_file = "cleaned_data.csv"
    df_clean.to_csv(output_file, index=False)
    print(f"\n=== 5. EXPORT COMPLETE ===")
    print(f"Cleaned data saved to: {output_file}")
    
    return df_clean

if __name__ == "__main__":
    if len(sys.argv)!= 2:
        print("Usage: python colab.py <your_file.csv>")
        print("Example: python colab.py sales_data.csv")
    else:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            clean_and_report(file_path)
        else:
            print(f"Error: File {file_path} not found")