from typing import Final, Dict, Any, Tuple

from pydantic import PositiveInt
from requests import Response

from ..ssl_context_session import SSLContextSession
from .utils import extract_filename

ONE_KB: Final[PositiveInt] = 1024


def download_file(url: str, *, json: Dict[str, Any]) -> str:
    assert url.startswith('https://')

    with SSLContextSession() as session:
        response, filename = _download_file(session, url, json)
        _write_to_file(response, filename)

    return filename

def _download_file(
    session: SSLContextSession,
    url: str,
    json: Dict[str, Any]
) -> Tuple[Response, str]:
    response = session.put(url, json=json, stream=True)
    response.raise_for_status()
    filename = extract_filename(response)

    return response, filename

def _write_to_file(response: Response, filename: str) -> None:
    with open(filename, mode='wb') as fh:
        chunk: bytes
        for chunk in response.iter_content(chunk_size=ONE_KB):
            fh.write(chunk)
