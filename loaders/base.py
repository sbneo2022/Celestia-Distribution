from abc import ABC, abstractmethod
from typing import Dict, Optional
import pandas as pd


class DataLoader(ABC):
    @abstractmethod
    def _get_files(self) -> Dict[str, str]:
        """Get available files for loading."""
        pass

    @abstractmethod
    def load_data(self, file_path: str) -> Optional[Dict[str, pd.DataFrame]]:
        """Load data from the specified file."""
        pass
