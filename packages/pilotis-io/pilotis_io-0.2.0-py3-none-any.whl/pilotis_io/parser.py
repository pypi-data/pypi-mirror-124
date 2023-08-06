import pandas as pd

from pilotis_io.persistence import LandingDataSourcePersistence


def parse_dataset(
    landing_persistence: LandingDataSourcePersistence, dataset_version: str
) -> None:
    dataset: pd.DataFrame = landing_persistence.load_raw(dataset_version)
    landing_persistence.save_parsed(dataset, dataset_version)
