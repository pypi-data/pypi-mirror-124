from pathlib import Path
from typing import Optional

from pilotis_io.exceptions import PilotisIoError

LANDING_ROOT_FOLDER_DIR_PATH = Path("landing")
USE_CASES_ROOT_FOLDER_DIR_PATH = Path("use_cases")


def dataset_raw_dir_path(
    dataset_name: Optional[str], dataset_version: Optional[str]
) -> Path:
    if dataset_name is None:
        raise PilotisIoError("Dataset name must be provided")
    if dataset_version is None:
        raise PilotisIoError("Dataset version must be provided")

    return LANDING_ROOT_FOLDER_DIR_PATH / "raw" / dataset_name / dataset_version


def dataset_parsed_dir_path(
    dataset_name: Optional[str], dataset_version: Optional[str]
) -> Path:
    if dataset_name is None:
        raise PilotisIoError("Dataset name must be provided")
    if dataset_version is None:
        raise PilotisIoError("Dataset version must be provided")

    return LANDING_ROOT_FOLDER_DIR_PATH / "parsed" / dataset_name / dataset_version


def dataset_use_case_dir_path(
    use_case_name: Optional[str],
    dataset_name: Optional[str],
    dataset_version: Optional[str],
) -> Path:
    if use_case_name is None:
        raise PilotisIoError("UseCase name must be provided")
    if dataset_name is None:
        raise PilotisIoError("Dataset name must be provided")
    if dataset_version is None:
        raise PilotisIoError("Dataset version must be provided")

    return (
        USE_CASES_ROOT_FOLDER_DIR_PATH
        / use_case_name
        / "datasets"
        / dataset_version
        / dataset_name
    )


def model_dir_path(
    use_case_name: Optional[str], model_name: Optional[str], run_id: Optional[str]
) -> Path:
    if use_case_name is None:
        raise PilotisIoError("UseCase name must be provided")
    if model_name is None:
        raise PilotisIoError("Model name must be provided")
    if run_id is None:
        raise PilotisIoError("Run ID must be provided")

    return (
        USE_CASES_ROOT_FOLDER_DIR_PATH / use_case_name / "models" / model_name / run_id
    )


def export_dir_path(
    use_case_name: Optional[str], export_name: Optional[str], run_id: Optional[str]
) -> Path:
    if use_case_name is None:
        raise PilotisIoError("UseCase name must be provided")
    if export_name is None:
        raise PilotisIoError("Export name must be provided")
    if run_id is None:
        raise PilotisIoError("Run ID must be provided")

    return (
        USE_CASES_ROOT_FOLDER_DIR_PATH
        / use_case_name
        / "exports"
        / export_name
        / run_id
    )
