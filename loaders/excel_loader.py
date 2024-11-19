# Standard library imports
import os
import pandas as pd
import streamlit as st
from typing import Dict, Optional

# Local imports
from .base import DataLoader
from sheet_processors.sheet_processors import (
    UnlockSheetProcessor,
    OverviewSheetProcessor,
    SupplySheetProcessor,
    IssuanceSheetProcessor,
    YieldSheetProcessor,
)


class ExcelDataLoader(DataLoader):
    """Loads and processes Excel files containing economic data.

    This class handles loading Excel files from a directory and processing each sheet
    using the appropriate sheet processor based on the sheet name.
    """

    def __init__(self):
        # Map sheet names to their corresponding processor instances
        self.processors = {
            "Unlock": UnlockSheetProcessor(),
            "Overview": OverviewSheetProcessor(),
            "Supply": SupplySheetProcessor(),
            "Issuance": IssuanceSheetProcessor(),
            "Relative-Yield": YieldSheetProcessor(),
            "Absolute-Yield": YieldSheetProcessor(),
        }
        self.excel_files = self._get_files()

    def _get_files(self) -> Dict[str, str]:
        """Get all Excel files from the excels directory.

        Returns:
            Dict mapping filenames to their full file paths
        """
        excel_dir = "excels"
        excel_files = {}

        if os.path.exists(excel_dir):
            for file in os.listdir(excel_dir):
                if file.endswith((".xlsx", ".xls")):
                    excel_files[file] = os.path.join(excel_dir, file)
        return excel_files

    @st.cache_data
    def load_data(_self, file_path: str) -> Optional[Dict[str, pd.DataFrame]]:
        """Load and process data from an Excel file.

        Args:
            file_path: Path to the Excel file to load

        Returns:
            Dict mapping sheet names to processed DataFrames, or None if loading fails
        """
        try:
            excel_file = pd.ExcelFile(file_path)
            sheets = {}

            # Process each sheet in the Excel file
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)

                # Apply the appropriate processor if one exists for this sheet
                if sheet_name in _self.processors:
                    processor = _self.processors[sheet_name]
                    df = processor.process(df)

                sheets[sheet_name] = df
            return sheets
        except Exception as e:
            st.error(f"Error loading Excel file: {str(e)}")
            return None
