from pathlib import Path
from typing import List, Optional

import boto3
from pilotis_io.exceptions import PilotisIoError
from pilotis_io.io import IoAPI


class S3IoAPI(IoAPI):
    def __init__(self, bucket_name: str):
        super().__init__(f"s3://{bucket_name}")
        self.s3_client = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")
        self.bucket_name = bucket_name

    def file_exists(self, relative_path: Optional[Path]) -> bool:
        if relative_path is None:
            raise PilotisIoError("Path must be provided")

        bucket = self.s3_resource.Bucket(self.bucket_name)
        for obj in bucket.objects.all():
            if str(self.project_root_path / relative_path).endswith(obj.key):
                return True
        return False

    def store_file(
        self, local_file_path: Optional[Path], relative_output_path: Optional[Path]
    ) -> None:
        if local_file_path is None:
            raise PilotisIoError("Local path must be provided")
        if relative_output_path is None:
            raise PilotisIoError("Target path must be provided")
        if self.file_exists(relative_output_path):
            raise PilotisIoError(f"{relative_output_path} already exists")

        with local_file_path.open("rb") as local_file:
            chunk = local_file.read()

        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=str(self.project_root_path / relative_output_path),
            Body=chunk,
        )

    def copy_or_symlink_to_local(
        self, relative_path: Optional[Path], relative_local_paths_target: Optional[Path]
    ) -> Path:
        if relative_path is None:
            raise PilotisIoError("A path to download must be provided")
        if relative_local_paths_target is None:
            raise PilotisIoError("A local path to create copy must be provided")

        with relative_local_paths_target.open("wb") as local_file:
            self.s3_client.download_fileobj(
                Bucket=self.bucket_name,
                Key=str(self.project_root_path / relative_path),
                Fileobj=local_file,
            )
        return relative_local_paths_target

    def list_files_in_dir(self, relative_dir_path: Optional[Path]) -> List[Path]:
        def _file_name(s3_object_key: str) -> str:
            return s3_object_key.split("/")[-1]

        s3_response = self.s3_client.list_objects(
            Bucket=self.bucket_name, Prefix=str(relative_dir_path)
        )

        if "Contents" not in s3_response:
            raise PilotisIoError(f"No file to list in {relative_dir_path}")

        keys: List[str] = [s3_object["Key"] for s3_object in s3_response["Contents"]]
        return [Path(key) for key in keys if _file_name(key) != ""]

    def mk_dir(self, relative_dir_path: Optional[Path]) -> Path:
        # Mkdir is irrelevant in an object store like S3
        pass
