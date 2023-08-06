import shutil
from pathlib import Path
from typing import List, Optional

from pilotis_io.exceptions import PilotisIoError
from pilotis_io.io import IoAPI


class LocalIoApi(IoAPI):
    def file_exists(self, relative_path: Optional[Path]) -> bool:
        if relative_path is None:
            return False

        return (self.project_root_path / relative_path).exists()

    def store_file(
        self, local_file_path: Optional[Path], relative_output_path: Optional[Path]
    ) -> None:
        if local_file_path is None:
            raise PilotisIoError("A source path must be provided")
        if relative_output_path is None:
            raise PilotisIoError(
                "A destination path must be provided with arelative path"
            )

        self.mk_dir(relative_output_path.parent)
        absolute_output_path = self.project_root_path / relative_output_path
        shutil.move(local_file_path.absolute(), absolute_output_path)

    def copy_or_symlink_to_local(
        self,
        relative_local_path: Optional[Path],
        relative_local_paths_target: Optional[Path],
    ) -> Path:
        if relative_local_path is None:
            raise PilotisIoError("A symlink local path to create must be provided")
        absolute_local_path = self.project_root_path / relative_local_path
        if absolute_local_path.exists():
            raise PilotisIoError(
                f"Local path '{absolute_local_path}' already exist. "
                f"Could not create Symlink"
            )

        if relative_local_paths_target is None:
            raise PilotisIoError("A symlink's target must be provided")
        absolute_local_paths_target = (
            self.project_root_path / relative_local_paths_target
        )
        if not absolute_local_paths_target.exists():
            raise PilotisIoError(
                f"Symlink's target '{absolute_local_paths_target}' does not exist"
            )

        absolute_local_path.symlink_to(absolute_local_paths_target)
        return absolute_local_path

    def list_files_in_dir(self, relative_dir_path: Optional[Path]) -> List[Path]:
        if relative_dir_path is None:
            raise PilotisIoError("Directory path must be provided")

        absolute_dir_path = self.project_root_path / relative_dir_path
        absolute_paths = [
            path for path in absolute_dir_path.iterdir() if path.is_file()
        ]
        return [path.relative_to(self.project_root_path) for path in absolute_paths]

    def mk_dir(self, relative_dir_path: Optional[Path]) -> Path:
        if relative_dir_path is None:
            raise PilotisIoError("Directory path must be provided")

        full_path = self.project_root_path / relative_dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        return full_path
