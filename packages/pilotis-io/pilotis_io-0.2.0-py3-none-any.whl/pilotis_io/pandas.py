import abc
from pathlib import Path
from typing import List, Optional

import pandas as pd

from pilotis_io.io import IoAPI


class PandasApi:
    io_api: IoAPI

    def __init__(self, io_api: IoAPI) -> None:
        self.io_api = io_api

    @abc.abstractmethod
    def load_pandas_dataset(
        self, relative_file_paths: Optional[List[Path]], *args, **kwargs
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abc.abstractmethod
    def save_pandas_dataset(
        self, df: pd.DataFrame, relative_export_path: Optional[Path]
    ) -> None:
        raise NotImplementedError
