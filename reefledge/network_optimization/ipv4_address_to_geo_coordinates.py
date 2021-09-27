from typing import Tuple, Dict, Optional as Opt, Union

import requests

PAIR = Tuple[float, float]
MAPPING = Dict[str, str]


def ipv4_address_to_geo_coordinates(ipv4_address: Opt[str] = None) -> PAIR:
    url = _get_url(ipv4_address)

    data: Union[str, MAPPING]
    data = requests.get(url).text.strip()
    data = eval(data)

    geo_coordinates: Union[str, PAIR]
    geo_coordinates = '(' + data['loc'] + ')'
    geo_coordinates = eval(geo_coordinates)

    return geo_coordinates

def _get_url(ipv4_address: Opt[str]) -> str:
    url = 'http://ipinfo.io/'

    if ipv4_address is not None:
        url += f"{ipv4_address}/"

    url += 'json'
    return url
