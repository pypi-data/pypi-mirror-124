from pathlib import Path
from typing import Optional

import numpy as np

from pilotis_io.exceptions import PilotisIoError
from pilotis_io.numpy import NumpyApi


class LocalNumpyApi(NumpyApi):
    def save_numpy_array(
        self, array: np.ndarray, relative_export_path: Optional[Path]
    ) -> None:
        if relative_export_path is None:
            raise PilotisIoError("An export path must be provided")

        if relative_export_path.suffix.lower() == ".npz":
            np.savez(self.io_api.get_path_uri(relative_export_path), array)
        else:
            raise PilotisIoError("Extension not supported for numpy saving")

    def load_numpy_array(self, relative_file_path: Optional[Path]) -> np.ndarray:
        if relative_file_path is None:
            raise PilotisIoError("A file path must be provided to load Numpy array")
        absolute_export_path = self.io_api.project_root_path / relative_file_path
        if not absolute_export_path.exists():
            raise PilotisIoError(
                f"Provided path does not exist: {absolute_export_path}"
            )
        return np.load(str(absolute_export_path))["arr_0"]
