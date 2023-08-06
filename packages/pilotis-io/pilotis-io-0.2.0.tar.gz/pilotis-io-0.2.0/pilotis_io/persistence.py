import abc
from pathlib import Path
from typing import List, Optional

import joblib
import pandas as pd
from sklearn.base import BaseEstimator

from pilotis_io import directory_structure
from pilotis_io.directory_structure import (
    dataset_use_case_dir_path,
    export_dir_path,
    model_dir_path,
)
from pilotis_io.exceptions import PilotisIoError
from pilotis_io.io import IoAPI
from pilotis_io.pandas import PandasApi


class LandingDataSourcePersistence:
    def __init__(self, io_api: IoAPI, pandas_api: PandasApi, dataset_name: str) -> None:
        self.io_api = io_api
        self.pandas_api = pandas_api
        self.dataset_name = dataset_name
        slug_dataset_name = self.dataset_name.lower().replace(" ", "_")
        self.parsed_file_name: str = f"{slug_dataset_name}.parquet"

    @abc.abstractmethod
    def load_raw(self, dataset_version: str = None) -> pd.DataFrame:
        raise NotImplementedError()

    def load_parsed(self, dataset_version: Optional[str]) -> pd.DataFrame:
        if dataset_version is None:
            raise PilotisIoError("Dataset version must be provided")

        return self.pandas_api.load_pandas_dataset(
            [
                directory_structure.dataset_parsed_dir_path(
                    self.dataset_name, dataset_version
                )
                / self.parsed_file_name
            ]
        )

    def save_parsed(self, dataset: pd.DataFrame, dataset_version: str):
        export_path: Path = (
            directory_structure.dataset_parsed_dir_path(
                self.dataset_name, dataset_version
            )
            / self.parsed_file_name
        )
        self.pandas_api.save_pandas_dataset(
            df=dataset, relative_export_path=export_path
        )

    def list_raw_files(self, dataset_version: Optional[str]) -> List[Path]:
        raw_dir_path = directory_structure.dataset_raw_dir_path(
            self.dataset_name, dataset_version
        )
        return self.io_api.list_files_in_dir(raw_dir_path)


class UseCaseDataSetPersistence:
    def __init__(
        self,
        io_api: IoAPI,
        pandas_api: PandasApi,
        use_case_name: str,
        dataset_name: str,
    ) -> None:
        self.io_api = io_api
        self.pandas_api = pandas_api
        self.use_case_name = use_case_name
        self.dataset_name = dataset_name

    def save_dataset(self, dataset: pd.DataFrame, dataset_version: str) -> None:
        self.pandas_api.save_pandas_dataset(
            df=dataset, relative_export_path=self.dataset_path(dataset_version)
        )

    def dataset_path(self, dataset_version: str) -> Path:
        dir_path = dataset_use_case_dir_path(
            self.use_case_name, self.dataset_name, dataset_version
        )
        return dir_path / f"{self.dataset_name.lower().replace(' ', '')}.parquet"

    def load_dataset(self, dataset_version: str) -> pd.DataFrame:
        return self.pandas_api.load_pandas_dataset([self.dataset_path(dataset_version)])


class UseCaseModelPersistence:
    def __init__(
        self,
        io_api: IoAPI,
        use_case_name: str,
        model_name: str,
        file_name: str = "model.pkl",
    ) -> None:
        self.io_api = io_api
        self.use_case_name = use_case_name
        self.model_name = model_name
        self.file_name = file_name

    def save_sklearn_model(self, model: BaseEstimator, model_run_id: str) -> None:
        model_local_copy_path: Path = Path("model.pkl")
        joblib.dump(model, model_local_copy_path)

        self.io_api.store_file(
            local_file_path=model_local_copy_path,
            relative_output_path=self.model_path(model_run_id),
        )

    def model_path(self, model_run_id: str) -> Path:
        model_dir = model_dir_path(self.use_case_name, self.model_name, model_run_id)
        return model_dir / self.file_name

    def load_sklearn_model(self, model_run_id: str) -> BaseEstimator:
        model_local_copy_path: Path = self.io_api.copy_or_symlink_to_local(
            relative_local_paths_target=self.model_path(model_run_id),
            relative_local_path=Path("model.pkl"),
        )

        model = joblib.load(model_local_copy_path.resolve())
        model_local_copy_path.unlink()
        return model


class UseCaseExportPersistence:
    def __init__(
        self,
        io_api: IoAPI,
        pandas_api: PandasApi,
        use_case_name: str,
        export_name: str,
        export_file_name: str = "export.csv",
    ) -> None:
        self.io_api = io_api
        self.pandas_api = pandas_api
        self.use_case_name = use_case_name
        self.export_name = export_name
        self.export_file_name = export_file_name

    def export_pandas_dataframe(self, export_df: pd.DataFrame, export_id: str) -> None:
        self.pandas_api.save_pandas_dataset(export_df, self.export_path(export_id))

    def export_path(self, export_id: str) -> Path:
        export_dir = export_dir_path(self.use_case_name, self.export_name, export_id)
        return export_dir / self.export_file_name

    def reload_pandas_export(self, export_id: str) -> pd.DataFrame:
        return self.pandas_api.load_pandas_dataset([self.export_path(export_id)])
