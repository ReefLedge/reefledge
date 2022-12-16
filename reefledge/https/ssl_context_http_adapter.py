from typing import final, Any
import ssl

from requests.adapters import HTTPAdapter


@final
class SSLContextHTTPAdapter(HTTPAdapter):

    check_hostname: bool

    def __init__(
        self,
        check_hostname: bool,
        *args: Any,
        **kwargs: Any
    ) -> None:
        self.check_hostname = check_hostname
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args: Any, **kwargs: Any) -> Any:
        ssl_context: ssl.SSLContext = ssl.create_default_context()
        ssl_context.check_hostname = self.check_hostname

        kwargs['ssl_context'] = ssl_context
        return super().init_poolmanager(*args, **kwargs) # type: ignore [no-untyped-call]
