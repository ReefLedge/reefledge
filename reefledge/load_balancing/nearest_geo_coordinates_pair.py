from typing import List, Tuple, Final
from math import radians, sin, cos, asin, sqrt

import numpy as np

from .ipv4_address_to_geo_coordinates import ipv4_address_to_geo_coordinates


class NearestGeoCoordinatesPair():

    target_geo_coordinates_pairs: List[Tuple[float, float]]
    host_geo_coordinates_pair: Tuple[float, float]

    def __init__(
        self, target_geo_coordinates_pairs: List[Tuple[float, float]]) -> None:
        #######################################################################
        self.target_geo_coordinates_pairs = target_geo_coordinates_pairs
        self.host_geo_coordinates_pair = ipv4_address_to_geo_coordinates()


    @property
    def index(self) -> int:
        distances: List[float] = []
        self._compute_distances(distances)

        return np.argmin(distances)

    def _compute_distances(self, distances: List[float]) -> None:
        for target_geo_coordinates_pair in self.target_geo_coordinates_pairs:
            haversine_dist = self.__class__.haversine_distance([
                self.host_geo_coordinates_pair,
                target_geo_coordinates_pair,
            ])

            distances.append(haversine_dist)


    @staticmethod
    def haversine_distance(pairs: List[Tuple[float, float]], /) -> float:
        assert len(pairs) == 2
        R: Final[float] = 6371 # Radius of earth in kilometers.

        # (latitude, longitude)
        y1, x1 = pairs[0]
        y2, x2 = pairs[1]

        # Convert degrees to radians.
        y1, x1, y2, x2 = map(radians, [y1, x1, y2, x2])

        dx = x2 - x1
        dy = y2 - y1

        # Haversine formula.
        a  = sin(dy/2)**2
        a += cos(y1) * cos(y2) * sin(dx/2)**2
        c  = 2 * asin(sqrt(a))

        return c*R
