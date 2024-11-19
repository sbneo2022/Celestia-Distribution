from abc import ABC, abstractmethod
import pandas as pd


class SheetProcessor(ABC):
    """Abstract base class for Excel sheet processors.

    Defines interface for processing different types of Excel sheets in the
    Economic Model. Each sheet type should implement its own processing logic.
    """

    @abstractmethod
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process a DataFrame according to sheet-specific rules.

        Args:
            df: Input DataFrame containing raw sheet data.

        Returns:
            Processed DataFrame with standardized format and cleaned data.
        """
        pass
