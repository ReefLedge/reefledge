from typing import List, Tuple

from requests import Response


def extract_filename(response: Response) -> str:
    content_disposition: str = response.headers['content-disposition']
    content_disposition_split: List[str] = content_disposition.split('; ')

    key_value_pair: str
    for key_value_pair in content_disposition_split:
        if key_value_pair.startswith(target_prefix:='filename='):
            raw_filename = key_value_pair[len(target_prefix):]
            return _parse_filename(raw_filename)
    else:
        assert False # Unreachable

def _parse_filename(raw_filename: str) -> str:
    quotes: Tuple[str, str] = ('"', "'")
    filename: str = raw_filename

    if filename.startswith(quotes):
        filename = filename[1:]

    if filename.endswith(quotes):
        filename = filename[:-1]

    return filename
