from typing import Tuple, Optional as Opt, Dict, Union, List, cast

import requests

PAIR = Tuple[float, float]


def ipv4_address_to_geo_coordinates(ipv4_address: Opt[str] = None) -> PAIR:
    data = _get_data_in_json_format(ipv4_address)
    geo_coordinates = _extract_geo_coordinates(data)

    return geo_coordinates


def _get_data_in_json_format(ipv4_address: Opt[str]) -> Dict[str, str]:
    url: str = __assemble_url(ipv4_address)
    response = requests.get(url)
    return response.json()

def __assemble_url(ipv4_address: Opt[str]) -> str:
    url: str = 'http://ipinfo.io/' # Not HTTPS

    if ipv4_address is not None:
        url += f"{ipv4_address}/"

    url += 'json'
    return url


def _extract_geo_coordinates(data: Dict[str, str]) -> PAIR:
    geo_coordinates: Union[List[str], PAIR]
    geo_coordinates = data['loc'].split(',') # list[str]
    assert len(geo_coordinates) == 2

    geo_coordinates = cast(
        PAIR,
        tuple([float(c) for c in geo_coordinates])
    )

    return geo_coordinates
