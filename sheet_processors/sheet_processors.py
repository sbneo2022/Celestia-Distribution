from .base import SheetProcessor
import pandas as pd


class UnlockSheetProcessor(SheetProcessor):
    """Process Unlock sheet with token distribution schedule.


    Handles duplicate columns, adds Cumulative prefix where needed,
    and standardizes date/month columns. Fix headers and removes first emty row.
    """

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        # Get the first row as column headers
        new_columns = df.iloc[0].tolist()

        # Handle duplicates by adding "Cumulative" prefix to second occurrence
        seen = {}
        for i, col in enumerate(new_columns):
            if col in seen:
                if col == "Cumulative":
                    new_columns[i] = f"{col} Emission"
                    continue

                new_columns[i] = f"Cumulative {col}"
            else:
                seen[col] = True

        # Set the processed columns and remove header rows
        df.columns = new_columns
        df = df.iloc[2:].reset_index(drop=True)

        # Drop duplicate date columns, keeping only the first
        date_columns = [col for col in df.columns if "Date" in str(col)]
        if len(date_columns) > 1:
            df = df.drop(columns=date_columns[1:])
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date

        # Standardize month column name and clean data
        df.rename(columns={df.columns[0]: "Month"}, inplace=True)
        return df.dropna(axis=1, how="all")


class OverviewSheetProcessor(SheetProcessor):
    """Process Overview sheet containing summary statistics.

    Fix headers and removes first emty row.
    """

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        df.rename(columns={df.columns[1]: "Value"}, inplace=True)
        df = df.dropna(how="all")  # Remove empty rows
        return df.dropna(axis=1, how="all")  # Remove empty columns


class SupplySheetProcessor(SheetProcessor):
    """Process Supply sheet with token supply data.

    Takes first 6 columns, standardizes headers, and cleans data.
    """

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.iloc[:, :6]  # Select first 6 columns
        df.columns = df.iloc[0]  # Use first row as headers
        df = df.iloc[2:].reset_index(drop=True)  # Remove header rows
        df.rename(columns={df.columns[0]: "Month"}, inplace=True)

        # Convert Date column to date without time if it exists
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date

        return df.dropna(axis=1, how="all")


class IssuanceSheetProcessor(SheetProcessor):
    """Process Issuance sheet with token issuance schedule.

    Fix headers and removes first emty row.
    """

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.iloc[0]  # Use first row as headers
        df.rename(columns={df.columns[0]: "Month"}, inplace=True)
        df = df.iloc[2:].reset_index(drop=True)  # Remove header rows

        # Rename issuance columns to include %
        if "Relative Issuance" in df.columns:
            df.rename(
                columns={"Relative Issuance": "Relative Issuance %"}, inplace=True
            )
        if "Absolute issuance" in df.columns:
            df.rename(
                columns={"Absolute issuance": "Absolute issuance %"}, inplace=True
            )

        # Convert Date column to date without time if it exists
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date

        return df.dropna(axis=1, how="all")


class YieldSheetProcessor(SheetProcessor):
    """Process Yield sheets (Relative/Absolute) with staking yields.

    Fix headers, removes first empty row, and converts float values to percentages.
    """

    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.iloc[0]  # Use first row as headers
        df = df.iloc[1:].reset_index(drop=True)  # Remove header row

        # Convert Date column to date without time if it exists
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date
        # Add % to column names for numeric columns except Date
        for col in df.columns:
            if col != "Date" and df[col].dtype in ["float64", "float32"]:
                df.rename(columns={col: f"{col*100:.0f}%"}, inplace=True)
        # Convert float columns to percentages
        for col in df.columns:
            if col != "Date" and df[col].dtype in ["float64", "float32"]:
                df[col] = df[col].multiply(100).round(3).astype(str) + "%"

        return df.dropna(axis=1, how="all")
