from typing import Any, Dict, Mapping, Optional, Tuple
import time

import backoff
import requests
from requests import session
from requests.exceptions import Timeout, ConnectionError, ChunkedEncodingError
from singer import get_logger, metrics

from tap_aftership.exceptions import (
    ERROR_CODE_EXCEPTION_MAPPING,
    AftershipError,
    AftershipRateLimitError,
    AftershipInternalServerError,
    AftershipServiceUnavailableError
)

LOGGER = get_logger()
REQUEST_TIMEOUT = 300

def raise_for_error(response: requests.Response) -> None:
    """Raises the associated response exception. Takes in a response object,
    checks the status code, and throws the associated exception based on the
    status code.

    :param resp: requests.Response object
    """
    try:
        response_json = response.json()
    except Exception:
        response_json = {}
    if response.status_code not in [200, 201, 204]:
        error_message = (
            response_json.get("error")
            or response_json.get("message")
            or response_json.get("meta", {}).get("message")
            or ERROR_CODE_EXCEPTION_MAPPING.get(response.status_code, {}).get("message", "Unknown Error")
        )

        message = f"HTTP-error-code: {response.status_code}, Error: {error_message}"
        exc = ERROR_CODE_EXCEPTION_MAPPING.get(response.status_code, {}).get(
            "raise_exception", AftershipError
        )
        raise exc(message, response) from None

def wait_if_retry_after(details):
    """Backoff handler that checks for a 'retry_after' attribute in the exception
    and sleeps for the specified duration to respect API rate limits.
    """
    exc = details['exception']
    if hasattr(exc, 'retry_after') and exc.retry_after is not None:
        LOGGER.warning(f"Rate limited. Retrying in {exc.retry_after} seconds...")
        time.sleep(exc.retry_after)

class Client:
    """
    A Wrapper class.
    ~~~
    Performs:
     - Authentication
     - Response parsing
     - HTTP Error handling and retry
    """

    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        self._session = session()
        self.base_url = "https://api.aftership.com"
        self.shipping_base_url = "https://api.aftership.com/postmen/v3"
        config_request_timeout = config.get("request_timeout")
        self.request_timeout = float(config_request_timeout) if config_request_timeout else REQUEST_TIMEOUT

    def __enter__(self):
        self.check_api_credentials()
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self._session.close()

    def check_api_credentials(self) -> None:
        pass

    def authenticate(self, headers: Dict, params: Dict) -> Tuple[Dict, Dict]:
        """Authenticates the request with the token"""
        headers["as-api-key"] = self.config["api_key"]
        return headers, params

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        path: Optional[str] = None
    ) -> Any:
        """
        Sends an HTTP request to the specified API endpoint.
        """
        params = params or {}
        headers = headers or {}
        body = body or {}
        endpoint = endpoint or f"{self.base_url}/{path}"
        headers, params = self.authenticate(headers, params)
        return self.__make_request(
            method, endpoint,
            headers=headers,
            params=params,
            data=body,
            timeout=self.request_timeout
        )

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(
            ConnectionResetError,
            ConnectionError,
            ChunkedEncodingError,
            Timeout,
            AftershipInternalServerError,
            AftershipServiceUnavailableError
        ),
        max_tries=5,
        factor=2,
    )
    @backoff.on_exception(
        wait_gen=backoff.constant,
        on_backoff=wait_if_retry_after,
        exception=(
            AftershipRateLimitError,
        ),
        max_tries=5,
        interval=1
    )
    def __make_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Optional[Mapping[Any, Any]]:
        """Performs HTTP Operations."""
        method = method.upper()
        with metrics.http_request_timer(endpoint):
            if method in ("GET", "POST"):
                if method == "GET":
                    kwargs.pop("data", None)
                response = self._session.request(method, endpoint, **kwargs)
                raise_for_error(response)
            else:
                raise ValueError(f"Unsupported method: {method}")

        return response.json()
