import abc
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from pilotis_io.exceptions import PilotisIoError


class IoAPI:
    def __init__(self, project_dir: str):
        self.project_root_url = urlparse(project_dir)
        if not self.project_root_url.scheme and not self.project_root_url.netloc:
            self.project_root_url = self.project_root_url._replace(
                path=(str(Path(project_dir).resolve()))
            )
        self.project_root_path = Path(self.project_root_url.path)

    def get_path_uri(self, path: Optional[Path]) -> str:
        if path is None:
            raise PilotisIoError("path must be provided")

        return self.project_root_url._replace(
            path=str(self.project_root_path / path)
        ).geturl()

    @abc.abstractmethod
    def file_exists(self, relative_path: Optional[Path]) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def store_file(
        self, local_file_path: Optional[Path], relative_output_path: Optional[Path]
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def copy_or_symlink_to_local(
        self,
        relative_local_path: Optional[Path],
        relative_local_paths_target: Optional[Path],
    ) -> Path:
        raise NotImplementedError

    @abc.abstractmethod
    def list_files_in_dir(self, relative_dir_path: Optional[Path]) -> List[Path]:
        raise NotImplementedError

    @abc.abstractmethod
    def mk_dir(self, relative_dir_path: Optional[Path]) -> Path:
        raise NotImplementedError
