import unittest
from parameterized import parameterized
import requests
from unittest.mock import patch, MagicMock
from requests.exceptions import Timeout, ConnectionError, ChunkedEncodingError
from tap_aftership.client import Client
from tap_aftership.exceptions import (
    AftershipBackoffError,
    AftershipBadRequestError,
    AftershipConflictError,
    AftershipError,
    AftershipForbiddenError,
    AftershipInternalServerError,
    AftershipNotFoundError,
    AftershipUnauthorizedError,
    AftershipUnprocessableEntityError,
    AftershipRateLimitError,
)

default_config = {
    "base_url": "https://api.example.com",
    "request_timeout": 30,
    "api_key": "dummy api key"
}

class MockResponse:
    def __init__(
            self,
            status_code,
            resp="",
            content=[""],
            headers=None,
            raise_error=True,
            text={}
        ):
        self.json_data = resp
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self.raise_error = raise_error
        self.text = text
        self.reason = "error"

    def raise_for_status(self):
        if not self.raise_error:
            return self.status_code
        raise requests.HTTPError("mock sample message")

    def json(self):
        return self.text

class TestClient(unittest.TestCase):

    def setUp(self):
        """Set up the client with default configuration."""
        self.client = Client(default_config)

    @parameterized.expand([
        ["empty string", "", 300.0],
        ["string value", "12", 12.0],
        ["int value", 10, 10.0],
        ["float value", 20.0, 20.0],
        ["zero value", 0, 300.0]
    ])
    @patch("tap_aftership.client.session")
    def test_client_initialization(self, name, input_value, expected_value, mock_session):
        """
        Test that the Client initializes the request_timeout attribute correctly from the config,
        and that it uses the 'session' object properly for HTTP requests.
        """
        config = default_config.copy()
        config["request_timeout"] = input_value
        client = Client(config)
        self.assertEqual(client.request_timeout, expected_value)
        self.assertIsInstance(client._session, mock_session().__class__)

    @parameterized.expand([
        ["GET request", "GET"],
        ["POST request", "POST"],
    ])
    @patch("tap_aftership.client.Client._Client__make_request", return_value={"data": "ok"})
    def test_client_make_request_mocked(self, name, method, mock_make_request):
        """
        Test that make_request returns data and calls __make_request correctly
        for both GET and POST methods.
        """
        client = Client(default_config)
        client.authenticate = MagicMock(return_value=({'as-api-key': 'Bearer test'}, {'limit': 1}))
        result = client.make_request(method, "https://api.example.com/resource", headers={})
        self.assertEqual(result, {"data": "ok"})
        mock_make_request.assert_called_once()

    @parameterized.expand([
        [
            "400 BadRequest",
            400,
            MockResponse(400, text={"message": "A validation exception has occurred."}),
            AftershipBadRequestError,
            "A validation exception has occurred."
        ],
        [
            "401 Unauthorized",
            401,
            MockResponse(401, text={"message": "The access token provided is expired, revoked, malformed or invalid for other reasons."}),
            AftershipUnauthorizedError,
            "The access token provided is expired, revoked, malformed or invalid for other reasons."
        ]
    ])
    def test_make_request_errors_without_retry(self, name, status_code, mock_resp, expected_exception, expected_message):
        """
        Test that __make_request raises correct exceptions for error codes without retry logic
        """
        client = Client(default_config)

        with patch.object(client._session, "request", return_value=mock_resp):
            with self.assertRaises(expected_exception) as context:
                client._Client__make_request("GET", "https://api.example.com/resource")

        self.assertIn(expected_message, str(context.exception))

    @parameterized.expand([
        ["ConnectionError", ConnectionError],
        ["Timeout", Timeout],
        ["ChunkedEncodingError", ChunkedEncodingError],
        ["InternalServerError", AftershipInternalServerError],
    ])
    def test_make_request_with_retry_on_connection_errors(self, name, exception_type):
        """
        Test that __make_request retries up to 5 times for retryable exceptions
        """
        client = Client(default_config)

        with patch.object(client._session, "request", side_effect=exception_type) as mock_request:
            with patch("time.sleep", return_value=None):
                with self.assertRaises(exception_type):
                    client._Client__make_request("GET", "https://api.example.com/resource")

        self.assertEqual(mock_request.call_count, 5)

    @parameterized.expand([
        ["400 error", 400, MockResponse(400), AftershipBadRequestError, "A validation exception has occurred."],
        ["401 error", 401, MockResponse(401), AftershipUnauthorizedError, "The access token provided is expired, revoked, malformed or invalid for other reasons."],
        ["403 error", 403, MockResponse(403), AftershipForbiddenError, "You are missing the following required scopes: read"],
        ["404 error", 404, MockResponse(404), AftershipNotFoundError, "The resource you have specified cannot be found."],
        ["409 error", 409, MockResponse(409), AftershipConflictError, "The API request cannot be completed because the requested operation would conflict with an existing item."],
        ["422 error", 422, MockResponse(422), AftershipUnprocessableEntityError, "The request content itself is not processable by the server."],
    ])
    def test_make_request_http_failure_without_retry(self, test_name, error_code, mock_response, error, error_message):

        with patch.object(self.client._session, "request", return_value=mock_response) as mock_request:
            with self.assertRaises(error) as e:
                self.client._Client__make_request("GET", "https://api.example.com/resource")

        expected_error_message = (f"HTTP-error-code: {error_code}, Error: {error_message}")
        self.assertEqual(str(e.exception), expected_error_message)
        self.assertEqual(mock_request.call_count, 1)

    @parameterized.expand([
        ["429 error", 429, MockResponse(429), AftershipRateLimitError, "The API rate limit for your organisation/application pairing has been exceeded. (Retry after 1 seconds.)"],
        ["500 error", 500, MockResponse(500), AftershipInternalServerError, "The server encountered an unexpected condition which prevented it from fulfilling the request."],
    ])
    @patch("time.sleep")
    def test_make_request_http_failure_with_retry(self, test_name, error_code, mock_response, error, error_message, mock_sleep):

        with patch.object(self.client._session, "request", return_value=mock_response) as mock_request:
            with self.assertRaises(error) as e:
                self.client._Client__make_request("GET", "https://api.example.com/resource")

            expected_error_message = (f"HTTP-error-code: {error_code}, Error: {error_message}")
            self.assertEqual(str(e.exception), expected_error_message)
            self.assertEqual(mock_request.call_count, 5)

    @parameterized.expand([
        ["ConnectionResetError", ConnectionResetError],
        ["ConnectionError", ConnectionError],
        ["ChunkedEncodingError", ChunkedEncodingError],
        ["Timeout", Timeout],
    ])
    @patch("time.sleep")
    def test_make_request_other_failure_with_retry(self, test_name, error, mock_sleep):

        with patch.object(self.client._session, "request", side_effect=error) as mock_request:
            with self.assertRaises(error) as e:
                self.client._Client__make_request("GET", "https://api.example.com/resource")

            self.assertEqual(mock_request.call_count, 5)

    @parameterized.expand([
        ["501 error - Not Implemented", 501, "Unknown Error"],
        ["502 error - Bad Gateway", 502, "Unknown Error"],
        ["503 error - Service Unavailable", 503, "Unknown Error"],
        ["504 error - Gateway Timeout", 504, "Unknown Error"],
        ["505 error - HTTP Version Not Supported", 505, "Unknown Error"],
        ["506 error - Variant Also Negotiates", 506, "Unknown Error"],
        ["507 error - Insufficient Storage", 507, "Unknown Error"],
        ["508 error - Loop Detected", 508, "Unknown Error"],
        ["509 error - Bandwidth Limit Exceeded", 509, "Unknown Error"],
        ["510 error - Not Extended", 510, "Unknown Error"],
        ["511 error - Network Authentication Required", 511, "Unknown Error"],
    ])
    @patch("time.sleep")
    def test_unmapped_5xx_errors_trigger_backoff(self, test_name, error_code, error_message, mock_sleep):
        """Test that unmapped 5xx errors trigger backoff retry as AftershipBackoffError."""
        mock_response = MockResponse(error_code)

        with patch.object(self.client._session, "request", return_value=mock_response) as mock_request:
            with self.assertRaises(AftershipBackoffError) as e:
                self.client._Client__make_request("GET", "https://api.example.com/resource")

            expected_error_message = f"HTTP-error-code: {error_code}, Error: {error_message}"
            self.assertEqual(str(e.exception), expected_error_message)
            # Verify backoff retry happened - should retry 5 times
            self.assertEqual(mock_request.call_count, 5)

    @parameterized.expand([
        # Below 5xx range — AftershipError, no retry
        ["status_499", 499, AftershipError, 1],
        # All 5xx errors (500-599) — AftershipBackoffError, retried
        ["status_500", 500, AftershipBackoffError, 5],
        ["status_550", 550, AftershipBackoffError, 5],
        ["status_599", 599, AftershipBackoffError, 5],
        # Above 5xx range — AftershipError, no retry
        ["status_600", 600, AftershipError, 1],
    ])
    @patch("time.sleep")
    def test_5xx_range_boundary_checks(self, test_name, status_code, expected_exception, expected_call_count, mock_sleep):
        """Test that the correct exception is raised at 5xx range boundaries."""
        mock_response = MockResponse(status_code)

        with patch.object(self.client._session, "request", return_value=mock_response) as mock_request:
            with self.assertRaises(expected_exception):
                self.client._Client__make_request("GET", "https://api.example.com/resource")

            # Verify retry behavior
            self.assertEqual(mock_request.call_count, expected_call_count)
