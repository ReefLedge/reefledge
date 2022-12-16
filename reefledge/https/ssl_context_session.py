from typing import final

from requests import Session

from .ssl_context_http_adapter import SSLContextHTTPAdapter


@final
class SSLContextSession(Session):

    def __init__(self, check_hostname: bool = True) -> None:
        super().__init__()

        self.mount(
            prefix='https://',
            adapter=SSLContextHTTPAdapter(check_hostname)
        )
