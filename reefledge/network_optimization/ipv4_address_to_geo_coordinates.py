from typing import Tuple, Optional as Opt, Dict, Union, List

import requests

PAIR = Tuple[float, float]


def ipv4_address_to_geo_coordinates(ipv4_address: Opt[str] = None) -> PAIR:
    url: str = _get_url(ipv4_address)
    response = requests.get(url)
    data: Dict[str, str] = response.json()

    geo_coordinates: Union[List[str], PAIR]
    geo_coordinates = data['loc'].split(',')
    geo_coordinates = tuple([float(c) for c in geo_coordinates])

    return geo_coordinates

def _get_url(ipv4_address: Opt[str]) -> str:
    url: str = 'https://ipinfo.io/'

    if ipv4_address is not None:
        url += f"{ipv4_address}/"

    url += 'json'
    return url
