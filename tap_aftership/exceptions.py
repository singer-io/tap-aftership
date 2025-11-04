import time


class AftershipError(Exception):
    """class representing Generic Http error."""

    def __init__(self, message=None, response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class AftershipBackoffError(AftershipError):
    """class representing backoff error handling."""
    pass

class AftershipBadRequestError(AftershipError):
    """class representing 400 status code."""
    pass

class AftershipUnauthorizedError(AftershipError):
    """class representing 401 status code."""
    pass


class AftershipForbiddenError(AftershipError):
    """class representing 403 status code."""
    pass

class AftershipNotFoundError(AftershipError):
    """class representing 404 status code."""
    pass

class AftershipConflictError(AftershipError):
    """class representing 409 status code."""
    pass

class AftershipUnprocessableEntityError(AftershipBackoffError):
    """class representing 422 status code."""
    pass

class AftershipRateLimitError(AftershipBackoffError):
    """class representing 429 status code."""
    def __init__(self, message=None, response=None):
        """Initialize the AftershipRateLimitError. Parses the 'rateLimit-reset' response (if present) and sets the
            `rateLimit-reset` attribute accordingly.
        """
        self.response = response
        self.retry_after = None
        self.limit = None
        self.remaining = None

        if response is not None:
            headers = response.headers or {}

            limit_keys = [
                "x-ratelimit-limit",
                "X-RateLimit-Limit",
                "ratelimit-limit"
            ]
            remaining_keys = [
                "x-ratelimit-remaining",
                "X-RateLimit-Remaining",
                "ratelimit-remaining"
            ]
            reset_keys = [
                "x-ratelimit-reset",
                "X-RateLimit-Reset",
                "ratelimit-reset"
            ]

            self.limit = self._get_header_int(headers, limit_keys, default=10)
            self.remaining = self._get_header_int(headers, remaining_keys, default=0)
            reset_ts = self._get_header_int(headers, reset_keys, default=0)

            if reset_ts:
                self.retry_after = max(0, int(reset_ts - time.time()))
            else:
                self.retry_after = 1

        base_msg = message or "AfterShip API rate limit exhausted"
        retry_info = (
            f"(Retry after {self.retry_after} seconds.)"
            if self.retry_after is not None
            else "(Retry after unknown delay.)"
        )
        full_message = f"{base_msg} {retry_info}"
        super().__init__(full_message, response=response)

    def _get_header_int(headers, keys, default=0):
        """Try to get the first valid integer value from a list of header keys."""
        for key in keys:
            val = headers.get(key)
            if val is not None:
                try:
                    return int(val)
                except (ValueError, TypeError):
                    break
        return default

class AftershipInternalServerError(AftershipBackoffError):
    """class representing 500 status code."""
    pass

class AftershipNotImplementedError(AftershipBackoffError):
    """class representing 501 status code."""
    pass

class AftershipBadGatewayError(AftershipBackoffError):
    """class representing 502 status code."""
    pass

class AftershipServiceUnavailableError(AftershipBackoffError):
    """class representing 503 status code."""
    pass

ERROR_CODE_EXCEPTION_MAPPING = {
    400: {
        "raise_exception": AftershipBadRequestError,
        "message": "A validation exception has occurred."
    },
    401: {
        "raise_exception": AftershipUnauthorizedError,
        "message": "The access token provided is expired, revoked, malformed or invalid for other reasons."
    },
    403: {
        "raise_exception": AftershipForbiddenError,
        "message": "You are missing the following required scopes: read"
    },
    404: {
        "raise_exception": AftershipNotFoundError,
        "message": "The resource you have specified cannot be found."
    },
    409: {
        "raise_exception": AftershipConflictError,
        "message": "The API request cannot be completed because the requested operation would conflict with an existing item."
    },
    422: {
        "raise_exception": AftershipUnprocessableEntityError,
        "message": "The request content itself is not processable by the server."
    },
    429: {
        "raise_exception": AftershipRateLimitError,
        "message": "The API rate limit for your organisation/application pairing has been exceeded."
    },
    500: {
        "raise_exception": AftershipInternalServerError,
        "message": "The server encountered an unexpected condition which prevented" \
            " it from fulfilling the request."
    },
    501: {
        "raise_exception": AftershipNotImplementedError,
        "message": "The server does not support the functionality required to fulfill the request."
    },
    502: {
        "raise_exception": AftershipBadGatewayError,
        "message": "Server received an invalid response."
    },
    503: {
        "raise_exception": AftershipServiceUnavailableError,
        "message": "API service is currently unavailable."
    }
}
