import abc
from pathlib import Path
from typing import Optional

import numpy as np

from pilotis_io.io import IoAPI


class NumpyApi:
    io_api: IoAPI

    def __init__(self, io_api: IoAPI) -> None:
        self.io_api = io_api

    @abc.abstractmethod
    def save_numpy_array(
        self, array: np.ndarray, relative_export_path: Optional[Path]
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def load_numpy_array(self, relative_file_path: Optional[Path]) -> np.ndarray:
        raise NotImplementedError
