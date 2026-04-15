import unittest
from unittest.mock import patch, MagicMock, mock_open

from tap_aftership.schema import get_schemas
from tap_aftership.exceptions import AftershipForbiddenError

SUCCESS_RESPONSE = {"meta": {"code": 200, "message": "ok"}}


def _make_stream_cls(parent="", check_access_response=None, check_access_raises=None):
    """
    Build a minimal mock stream *class* that get_schemas can iterate over and
    instantiate.

    Class-level attributes (parent, replication_keys, …) are consumed by
    get_schemas before instantiation; instance-level ``check_access`` controls
    the 403 / OK branch.
    """
    cls = MagicMock()
    # Class-level attributes read before instantiation
    cls.parent = parent
    cls.replication_keys = []
    cls.key_properties = ["id"]
    cls.replication_method = "FULL_TABLE"

    # Instance returned when the class is called with client=...
    instance = cls.return_value
    instance.parent = parent
    if check_access_raises is not None:
        instance.check_access.side_effect = check_access_raises
    else:
        instance.check_access.return_value = (
            check_access_response if check_access_response is not None else SUCCESS_RESPONSE
        )
    return cls


class TestGetSchemas(unittest.TestCase):
    """Unit tests for tap_aftership.schema.get_schemas."""

    def setUp(self):
        self.client = MagicMock()

        # Patch every external dependency so tests never touch the filesystem,
        # the singer library internals, or real HTTP calls.
        self._patchers = [
            patch(
                "tap_aftership.schema.load_schema_references",
                return_value={},
            ),
            patch(
                "tap_aftership.schema.singer.resolve_schema_references",
                side_effect=lambda schema, refs: schema,
            ),
            patch(
                "builtins.open",
                mock_open(read_data='{"properties": {}}'),
            ),
            patch("tap_aftership.schema.metadata.new", return_value={}),
            patch("tap_aftership.schema.metadata.get_standard_metadata", return_value=[]),
            patch("tap_aftership.schema.metadata.to_map", return_value={}),
            patch("tap_aftership.schema.metadata.write", return_value={}),
            patch("tap_aftership.schema.metadata.to_list", return_value=[]),
        ]
        for p in self._patchers:
            p.start()

    def tearDown(self):
        for p in self._patchers:
            p.stop()

    def _run(self, streams_dict):
        """Invoke get_schemas with a controlled STREAMS dict."""
        with patch("tap_aftership.schema.STREAMS", streams_dict):
            return get_schemas(self.client)

    def test_all_streams_accessible_returns_all_schemas(self):
        """All streams that pass check_access appear in the returned catalog."""
        stores_cls = _make_stream_cls(parent="")
        orders_cls = _make_stream_cls(parent="stores")  # child – check_access skipped

        schemas, mdata = self._run({"stores": stores_cls, "orders": orders_cls})

        self.assertIn("stores", schemas)
        self.assertIn("orders", schemas)
        self.assertEqual(len(schemas), 2)

    def test_check_access_called_only_for_parent_streams(self):
        """check_access must be invoked for parent streams and skipped for children."""
        stores_cls = _make_stream_cls(parent="")
        orders_cls = _make_stream_cls(parent="stores")

        self._run({"stores": stores_cls, "orders": orders_cls})

        # Parent stream → called once
        stores_cls.return_value.check_access.assert_called_once()
        # Child stream → never called
        orders_cls.return_value.check_access.assert_not_called()

    def test_forbidden_parent_stream_excluded_from_catalog(self):
        """A parent stream that raises AftershipForbiddenError is removed from
        both schemas and field_metadata."""
        ok_cls = _make_stream_cls(parent="")
        forbidden_cls = _make_stream_cls(
            parent="", check_access_raises=AftershipForbiddenError("403")
        )

        schemas, mdata = self._run({"ok_stream": ok_cls, "forbidden_stream": forbidden_cls})

        self.assertIn("ok_stream", schemas)
        self.assertNotIn("forbidden_stream", schemas)
        self.assertNotIn("forbidden_stream", mdata)

    def test_all_parent_streams_forbidden_raises_forbidden_error(self):
        """When every parent stream is unauthorized AftershipForbiddenError is raised."""
        forbidden_cls = _make_stream_cls(
            parent="", check_access_raises=AftershipForbiddenError("403")
        )

        with self.assertRaises(AftershipForbiddenError):
            self._run({"stores": forbidden_cls})

    def test_partial_403_logs_warning_without_raising(self):
        """When some (but not all) parent streams fail, a warning is issued and
        only the authorised streams are returned — no exception."""
        ok_cls = _make_stream_cls(parent="")
        forbidden_cls = _make_stream_cls(
            parent="", check_access_raises=AftershipForbiddenError("403")
        )

        # Should not raise
        schemas, _ = self._run({"allowed_stream": ok_cls, "forbidden_stream": forbidden_cls})

        self.assertIn("allowed_stream", schemas)
        self.assertNotIn("forbidden_stream", schemas)

    def test_children_excluded_when_parent_stream_is_forbidden(self):
        """Children of a 403-excluded parent are removed by orphan pruning."""
        stores_cls = _make_stream_cls(
            parent="", check_access_raises=AftershipForbiddenError("403")
        )
        orders_cls = _make_stream_cls(parent="stores")
        products_cls = _make_stream_cls(parent="stores")
        ok_cls = _make_stream_cls(parent="")  # keep error_list < total so no re-raise

        streams = {
            "stores": stores_cls,
            "orders": orders_cls,
            "products": products_cls,
            "ok_stream": ok_cls,
        }
        schemas, _ = self._run(streams)

        self.assertNotIn("stores", schemas)
        self.assertNotIn("orders", schemas)
        self.assertNotIn("products", schemas)
        self.assertIn("ok_stream", schemas)

    def test_grandchild_excluded_via_single_pass_orphan_pruning(self):
        """
        Validates that the single-pass pruning handles a 2-level hierarchy:
          stores (403) → orders (parent=stores) → fulfillments (parent=orders)

        Because STREAMS ordering is stores → orders → fulfillments, a single
        forward pass is sufficient:
          1. orders detected as orphan (stores missing) and removed
          2. fulfillments detected as orphan (orders now missing) and removed
        """
        stores_cls = _make_stream_cls(
            parent="", check_access_raises=AftershipForbiddenError("403")
        )
        orders_cls = _make_stream_cls(parent="stores")
        fulfillments_cls = _make_stream_cls(parent="orders")
        ok_cls = _make_stream_cls(parent="")  # keep error_list < total

        streams = {
            "stores": stores_cls,
            "orders": orders_cls,
            "fulfillments": fulfillments_cls,
            "ok_stream": ok_cls,
        }
        schemas, _ = self._run(streams)

        self.assertNotIn("stores", schemas)
        self.assertNotIn("orders", schemas)      # pruned: parent 'stores' excluded
        self.assertNotIn("fulfillments", schemas)  # pruned: parent 'orders' excluded
        self.assertIn("ok_stream", schemas)

    def test_child_not_pruned_when_parent_accessible(self):
        """Children are kept when their parent is accessible."""
        stores_cls = _make_stream_cls(parent="")
        orders_cls = _make_stream_cls(parent="stores")
        fulfillments_cls = _make_stream_cls(parent="orders")

        streams = {
            "stores": stores_cls,
            "orders": orders_cls,
            "fulfillments": fulfillments_cls,
        }
        schemas, _ = self._run(streams)

        self.assertIn("stores", schemas)
        self.assertIn("orders", schemas)
        self.assertIn("fulfillments", schemas)

    def test_success_response_with_code_20000(self):
        """Code 20000 is an accepted alternative success code."""
        stores_cls = _make_stream_cls(
            parent="",
            check_access_response={
                "meta": {"code": 20000, "message": "The request has been processed successfully."}
            },
        )

        schemas, _ = self._run({"stores": stores_cls})

        self.assertIn("stores", schemas)

    def test_success_response_without_meta_wrapper(self):
        """Responses with no 'meta' key fall back to top-level code/message."""
        stores_cls = _make_stream_cls(
            parent="",
            check_access_response={"code": 200, "message": "ok"},
        )

        schemas, _ = self._run({"stores": stores_cls})

        self.assertIn("stores", schemas)

    def test_non_success_code_and_message_excludes_stream(self):
        """A response with an unrecognised code and message triggers exclusion."""
        bad_cls = _make_stream_cls(
            parent="",
            check_access_response={"meta": {"code": 403, "message": "forbidden"}},
        )
        ok_cls = _make_stream_cls(parent="")

        schemas, _ = self._run({"ok_stream": ok_cls, "bad_stream": bad_cls})

        self.assertIn("ok_stream", schemas)
        self.assertNotIn("bad_stream", schemas)
