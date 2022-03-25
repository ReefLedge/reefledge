from typing import List, Tuple
from functools import cached_property

from ..ftp_client import FTPClientPublic
from ..network_optimization import NearestGeoCoordinatesPair


class OptimalRemoteZipFileFinder():

    target_remote_dir_name: str
    ftp_client: FTPClientPublic

    def __init__(
        self,
        target_remote_dir_name: List[str],
        ftp_client: FTPClientPublic) -> None:
        ################################################################
        self.target_remote_dir_name = '/'.join(target_remote_dir_name)
        self.ftp_client = ftp_client


    @cached_property
    def remote_zip_file_names(self) -> List[str]:
        return self.ftp_client.list_directory(self.target_remote_dir_name)

    @cached_property
    def geo_coordinates_pairs(self) -> List[Tuple[float, float]]:
        _geo_coordinates_pairs: List[Tuple[float, float]] = []

        for file_name in self.remote_zip_file_names:
            file_name_split = file_name[:-4].split('_')
            latitude = float(file_name_split[-2])
            longitude = float(file_name_split[-1])
            _geo_coordinates_pairs.append((latitude, longitude))

        return _geo_coordinates_pairs


    def find(self) -> str:
        return self.remote_zip_file_names[self.optimal_idx]

    @property
    def optimal_idx(self) -> int:
        return NearestGeoCoordinatesPair(self.geo_coordinates_pairs).index
