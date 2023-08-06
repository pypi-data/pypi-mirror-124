from pilotis_io.io import IoAPI
from pilotis_io.local import LocalPandasApi


class S3PandasAPi(LocalPandasApi):
    def __init__(self, io_api: IoAPI):
        super().__init__(io_api)
