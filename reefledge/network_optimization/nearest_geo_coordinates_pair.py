from typing import List, Tuple, Optional, Final
from functools import cached_property
from math import radians, sin, cos, asin, sqrt

import numpy as np
from pydantic import NonNegativeFloat

from .ipv4_address_to_geo_coordinates import ipv4_address_to_geo_coordinates


class NearestGeoCoordinatesPair():

    load_balanc_geo_coordinates_pairs: List[Tuple[float, float]]
    client_ipv4_address: Optional[str]

    def __init__(
        self,
        load_bal_geo_coordinates_pairs: List[Tuple[float, float]],
        client_ipv4_address: Optional[str]
    ) -> None:
        self.load_balanc_geo_coordinates_pairs = load_bal_geo_coordinates_pairs
        self.client_ipv4_address = client_ipv4_address

    @cached_property
    def client_geo_coordinates_pair(self) -> Tuple[float, float]:
        return ipv4_address_to_geo_coordinates(self.client_ipv4_address)


    @property
    def index(self) -> np.int64:
        distances: List[NonNegativeFloat] = []
        self._compute_distances(distances)

        return np.argmin(distances)

    def _compute_distances(self, distances: List[NonNegativeFloat]) -> None:
        for lb_geo_coordinates_pair in self.load_balanc_geo_coordinates_pairs:
            haversine_dist = self.__class__.haversine_distance([
                self.client_geo_coordinates_pair,
                lb_geo_coordinates_pair,
            ])

            distances.append(haversine_dist)


    @staticmethod
    def haversine_distance(
        pairs: List[Tuple[float, float]], /
    ) -> NonNegativeFloat:
        assert len(pairs) == 2
        R: Final[float] = 6371 # Radius of earth in kilometers.

        # (latitude, longitude)
        y0, x0 = pairs[0]
        y1, x1 = pairs[1]

        # Convert degrees to radians.
        y0, x0, y1, x1 = map(radians, [y0, x0, y1, x1])

        dx = x1 - x0
        dy = y1 - y0

        # Haversine formula.
        a  = sin(dy/2)**2
        a += cos(y0) * cos(y1) * sin(dx/2)**2
        c  = 2 * asin(sqrt(a))

        return c*R
