from typing import Final, Dict, Any

from pydantic import PositiveInt
from requests import Response

from ..ssl_context_session import SSLContextSession
from .utils import extract_filename

ONE_KB: Final[PositiveInt] = 1024


def download_file(url: str, *, json: Dict[str, Any]) -> str:
    assert url.startswith('https://')

    with SSLContextSession() as session:
        response = session.get(url, json=json, stream=True)
        filename = extract_filename(response)
        _write_to_file(response, filename)

    return filename

def _write_to_file(response: Response, filename: str) -> None:
    with open(filename, mode='wb') as fh:
        chunk: bytes
        for chunk in response.iter_content(chunk_size=ONE_KB):
            fh.write(chunk)
