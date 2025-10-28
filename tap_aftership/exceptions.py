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

            limit_val = (
                headers.get("x-ratelimit-limit")
                or headers.get("X-RateLimit-Limit")
                or headers.get("ratelimit-limit")
            )

            remaining_val = (
                headers.get("x-ratelimit-remaining")
                or headers.get("X-RateLimit-Remaining")
                or headers.get("ratelimit-remaining")
            )

            reset_val = (
                headers.get("x-ratelimit-reset")
                or headers.get("X-RateLimit-Reset")
                or headers.get("ratelimit-reset")
            )

            try:
                self.limit = int(limit_val) if limit_val is not None else 10
            except (ValueError, TypeError):
                self.limit = 10

            try:
                self.remaining = int(remaining_val) if remaining_val is not None else 0
            except (ValueError, TypeError):
                self.remaining = 0

            try:
                reset_ts = int(reset_val) if reset_val is not None else 0
                if reset_ts:
                    self.retry_after = max(0, int(reset_ts - time.time()))
            except (ValueError, TypeError):
                self.retry_after = 1

        base_msg = message or "AfterShip API rate limit exhausted"
        retry_info = (
            f"(Retry after {self.retry_after} seconds.)"
            if self.retry_after is not None
            else "(Retry after unknown delay.)"
        )
        full_message = f"{base_msg} {retry_info}"
        super().__init__(full_message, response=response)

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
