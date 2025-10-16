class aftershipError(Exception):
    """class representing Generic Http error."""

    def __init__(self, message=None, response=None):
        super().__init__(message)
        self.message = message
        self.response = response


class aftershipBackoffError(aftershipError):
    """class representing backoff error handling."""
    pass

class aftershipBadRequestError(aftershipError):
    """class representing 400 status code."""
    pass

class aftershipUnauthorizedError(aftershipError):
    """class representing 401 status code."""
    pass


class aftershipForbiddenError(aftershipError):
    """class representing 403 status code."""
    pass

class aftershipNotFoundError(aftershipError):
    """class representing 404 status code."""
    pass

class aftershipConflictError(aftershipError):
    """class representing 409 status code."""
    pass

class aftershipUnprocessableEntityError(aftershipBackoffError):
    """class representing 422 status code."""
    pass

class aftershipRateLimitError(aftershipBackoffError):
    """class representing 429 status code."""
    pass

class aftershipInternalServerError(aftershipBackoffError):
    """class representing 500 status code."""
    pass

class aftershipNotImplementedError(aftershipBackoffError):
    """class representing 501 status code."""
    pass

class aftershipBadGatewayError(aftershipBackoffError):
    """class representing 502 status code."""
    pass

class aftershipServiceUnavailableError(aftershipBackoffError):
    """class representing 503 status code."""
    pass

ERROR_CODE_EXCEPTION_MAPPING = {
    400: {
        "raise_exception": aftershipBadRequestError,
        "message": "A validation exception has occurred."
    },
    401: {
        "raise_exception": aftershipUnauthorizedError,
        "message": "The access token provided is expired, revoked, malformed or invalid for other reasons."
    },
    403: {
        "raise_exception": aftershipForbiddenError,
        "message": "You are missing the following required scopes: read"
    },
    404: {
        "raise_exception": aftershipNotFoundError,
        "message": "The resource you have specified cannot be found."
    },
    409: {
        "raise_exception": aftershipConflictError,
        "message": "The API request cannot be completed because the requested operation would conflict with an existing item."
    },
    422: {
        "raise_exception": aftershipUnprocessableEntityError,
        "message": "The request content itself is not processable by the server."
    },
    429: {
        "raise_exception": aftershipRateLimitError,
        "message": "The API rate limit for your organisation/application pairing has been exceeded."
    },
    500: {
        "raise_exception": aftershipInternalServerError,
        "message": "The server encountered an unexpected condition which prevented" \
            " it from fulfilling the request."
    },
    501: {
        "raise_exception": aftershipNotImplementedError,
        "message": "The server does not support the functionality required to fulfill the request."
    },
    502: {
        "raise_exception": aftershipBadGatewayError,
        "message": "Server received an invalid response."
    },
    503: {
        "raise_exception": aftershipServiceUnavailableError,
        "message": "API service is currently unavailable."
    }
}

