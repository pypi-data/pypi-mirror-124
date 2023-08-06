from pathlib import Path
from typing import List, Optional

import pandas as pd

from pilotis_io.exceptions import PilotisIoError
from pilotis_io.pandas import PandasApi


class LocalPandasApi(PandasApi):
    def load_pandas_dataset(
        self, relative_file_paths: Optional[List[Path]], *args, **kwargs
    ) -> pd.DataFrame:
        def load_df(path: Path):
            if path.suffix.lower() == ".csv":
                return pd.read_csv(self.io_api.get_path_uri(path), *args, **kwargs)
            elif path.suffix.lower() == ".parquet":
                return pd.read_parquet(self.io_api.get_path_uri(path), *args, **kwargs)
            else:
                raise PilotisIoError(
                    f"Format ${path.suffix[1:]} unknown. "
                    "Supported format are parquet and csv."
                )

        if relative_file_paths is None or len(relative_file_paths) == 0:
            raise PilotisIoError("A file path must be provided to load DataFrame")

        dfs = [load_df(path) for path in relative_file_paths]
        return pd.concat(dfs)

    def save_pandas_dataset(
        self, df: pd.DataFrame, relative_export_path: Optional[Path]
    ) -> None:
        if df is None:
            raise PilotisIoError("A dataframe must be provided when saving it.")
        if relative_export_path is None:
            raise PilotisIoError("An export path must be provided to export DataFrame")

        self.io_api.mk_dir(relative_export_path.parent)

        if relative_export_path.suffix.lower() == ".csv":
            return df.to_csv(
                self.io_api.get_path_uri(relative_export_path), index=False
            )
        elif relative_export_path.suffix.lower() == ".parquet":
            return df.to_parquet(
                self.io_api.get_path_uri(relative_export_path), index=False
            )
        else:
            raise PilotisIoError(
                f"Format ${relative_export_path.suffix[1:]} unknown. "
                "Supported format are parquet and csv."
            )
