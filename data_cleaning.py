"""
Data Cleaning Script
--------------------
This script:
1. Identifies missing values
2. Handles missing values
3. Converts columns to correct data types
4. Outputs a clean dataset ready for analysis
"""

import pandas as pd


def clean_dataset(file_path: str, output_path: str) -> None:
    """
    Cleans the dataset and saves the cleaned version.

    Parameters:
    file_path (str): Path to raw dataset
    output_path (str): Path to save cleaned dataset
    """

    # ---------------------------
    # 1. Load Dataset
    # ---------------------------
    df = pd.read_csv(file_path)

    print("\nInitial Missing Values:\n")
    print(df.isnull().sum())

    # ---------------------------
    # 2. Handle Missing Values
    # ---------------------------

    # Fill numeric columns with median
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Fill categorical columns with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    # ---------------------------
    # 3. Convert Date Columns
    # ---------------------------
    date_columns = [col for col in df.columns if "date" in col.lower()]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # ---------------------------
    # 4. Clean Currency Columns
    # ---------------------------
    currency_columns = ["Sales", "Profit"]

    for col in currency_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .replace(r"[\$,]", "", regex=True)
                .astype(float)
            )

    # Convert Quantity to numeric if needed
    if "Quantity" in df.columns:
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

    print("\nMissing Values After Cleaning:\n")
    print(df.isnull().sum())

    print("\nFinal Data Types:\n")
    print(df.dtypes)

    # ---------------------------
    # 5. Save Clean Dataset
    # ---------------------------
    df.to_csv(output_path, index=False)

    print(f"\nClean dataset saved to: {output_path}")


if __name__ == "__main__":
    clean_dataset(
        file_path="superstore.csv",
        output_path="superstore_cleaned.csv"
    )
