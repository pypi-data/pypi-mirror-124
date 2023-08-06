import os
from pathlib import Path
from typing import Optional

import numpy as np
from pilotis_io.exceptions import PilotisIoError
from pilotis_io.io import IoAPI
from pilotis_io.numpy import NumpyApi


class S3NumpyApi(NumpyApi):
    def __init__(self, io_api: IoAPI):
        super().__init__(io_api)

    def save_numpy_array(
        self, array: np.ndarray, relative_export_path: Optional[Path]
    ) -> None:
        if relative_export_path is None:
            raise PilotisIoError("An export path must be provided")

        local_copy_path = Path("array.copy.local.npz")

        if relative_export_path.suffix.lower() == ".npz":
            np.savez(local_copy_path, array)
        else:
            raise PilotisIoError("Extension not supported for numpy saving")

        self.io_api.store_file(local_copy_path, relative_export_path)
        os.remove(local_copy_path)

    def load_numpy_array(self, relative_file_path: Optional[Path]) -> np.ndarray:
        if relative_file_path is None:
            raise PilotisIoError("An export path must be provided")
        if not self.io_api.file_exists(relative_file_path):
            raise PilotisIoError(f"{relative_file_path} does not exists")

        local_copy_path = Path("array.copy.local")
        self.io_api.copy_or_symlink_to_local(relative_file_path, local_copy_path)
        result = np.load(str(local_copy_path))["arr_0"]
        local_copy_path.unlink()
        return result
