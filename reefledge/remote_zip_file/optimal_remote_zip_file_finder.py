from typing import Optional, List, Tuple
from functools import cached_property
import ftplib

import numpy as np

from ..ftp_client import FTPClientDownload
from ..network_optimization import NearestGeoCoordinatesPair


class OptimalRemoteZipFileFinder():

    target_remote_dir_name: str
    ftp_client: FTPClientDownload
    client_ipv4_address: Optional[str]

    def __init__(
        self,
        target_remote_directory_name: List[str],
        ftp_client: FTPClientDownload,
        client_ipv4_address: Optional[str]
    ) -> None:
        self.target_remote_dir_name = '/'.join(target_remote_directory_name)
        self.ftp_client = ftp_client
        self.client_ipv4_address = client_ipv4_address

    @cached_property
    def remote_zip_file_names(self) -> List[str]:
        return self.ftp_client.list_directory(self.target_remote_dir_name)


    @cached_property
    def geo_coordinates_pairs(self) -> List[Tuple[float, float]]:
        geo_coordinates_pairs_: List[Tuple[float, float]] = []

        zip_file_name: str
        for zip_file_name in self.remote_zip_file_names:
            pair = self._extract_geo_coordinates_pair(zip_file_name)
            geo_coordinates_pairs_.append(pair)

        return geo_coordinates_pairs_

    def _extract_geo_coordinates_pair(
        self,
        zip_file_name: str
    ) -> Tuple[float, float]:
        file_name_without_extension: str = zip_file_name[:-4]
        file_name_split: List[str] = file_name_without_extension.split('_')
        assert len(file_name_split) == 3

        latitude = float(file_name_split[-2])
        longitude = float(file_name_split[-1])

        return latitude, longitude


    def find(self) -> str:
        if len(self.remote_zip_file_names) > 0:
            return self.remote_zip_file_names[self.optimal_idx]
        else:
            dir_name = self.target_remote_dir_name
            raise ftplib.error_perm(f'Remote directory "{dir_name}" is empty.')

    @property
    def optimal_idx(self) -> np.int64:
        nearest_geo_coordinates_pair = NearestGeoCoordinatesPair(
            self.geo_coordinates_pairs,
            self.client_ipv4_address
        )

        return nearest_geo_coordinates_pair.index
