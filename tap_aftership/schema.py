import os
import json
import singer
from typing import Dict, Tuple
from singer import metadata
from tap_aftership.streams import STREAMS
from tap_aftership.exceptions import AftershipForbiddenError

LOGGER = singer.get_logger()


def get_abs_path(path: str) -> str:
    """
    Get the absolute path for the schema files.
    """
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schema_references() -> Dict:
    """
    Load the schema files from the schema folder and return the schema references.
    """
    shared_schema_path = get_abs_path("schemas/shared")

    shared_file_names = []
    if os.path.exists(shared_schema_path):
        shared_file_names = [
            f
            for f in os.listdir(shared_schema_path)
            if os.path.isfile(os.path.join(shared_schema_path, f))
        ]

    refs = {}
    for shared_schema_file in shared_file_names:
        with open(os.path.join(shared_schema_path, shared_schema_file)) as data_file:
            refs["shared/" + shared_schema_file] = json.load(data_file)

    return refs


def get_schemas(client) -> Tuple[Dict, Dict]:
    """
    Load the schema references, prepare metadata for each streams and return schema and metadata for the catalog.
    """
    schemas = {}
    field_metadata = {}
    error_list = []

    refs = load_schema_references()
    for stream_name, stream_obj in STREAMS.items():
        schema_path = get_abs_path("schemas/{}.json".format(stream_name))
        with open(schema_path) as file:
            schema = json.load(file)

        schemas[stream_name] = schema
        schema = singer.resolve_schema_references(schema, refs)

        mdata = metadata.new()
        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=getattr(stream_obj, "key_properties"),
            valid_replication_keys=(getattr(stream_obj, "replication_keys") or []),
            replication_method=getattr(stream_obj, "replication_method"),
        )
        mdata = metadata.to_map(mdata)

        automatic_keys = getattr(stream_obj, "replication_keys") or []
        for field_name in schema.get("properties", {}).keys():
            if field_name in automatic_keys:
                mdata = metadata.write(
                    mdata, ("properties", field_name), "inclusion", "automatic"
                )

        parent_tap_stream_id = getattr(stream_obj, "parent", None)
        if parent_tap_stream_id:
            mdata = metadata.write(mdata, (), 'parent-tap-stream-id', parent_tap_stream_id)
        mdata = metadata.to_list(mdata)
        field_metadata[stream_name] = mdata

        try:
            # Here it call the check_access method to check whether stream have read permission or not.
            # If stream does not have read permission then append that stream name to list and at the end of all streams
            # raise forbidden error with proper message containing stream names.
            stream_obj = stream_obj(client=client)
            if not stream_obj.parent:
                response = stream_obj.check_access()
                # Handle both response structures: with 'meta' key and without
                meta = response.get("meta", response)
                code = meta.get("code")
                message = meta.get("message", "").lower()

                # Accept multiple success codes (200, 20000) and success messages
                success_codes = {200, 20000}
                success_messages = {'ok', 'the request has been processed successfully.'}

                if code not in success_codes and message not in success_messages:
                    raise AftershipForbiddenError
        except AftershipForbiddenError:
            LOGGER.warning("Stream %s does not have read permission, excluding from catalog", stream_name)
            schemas.pop(stream_name, None)
            field_metadata.pop(stream_name, None)
            error_list.append(stream_name)

    # Single pass is sufficient because the hierarchy is at most 2 levels deep
    # (stores → orders/products → fulfillments) and all parent streams are checked
    # before their children in STREAMS ordering.
    for name, stream_cls in list(STREAMS.items()):
        if name in schemas and stream_cls.parent and stream_cls.parent not in schemas:
            LOGGER.warning(
                "Stream '%s' excluded from catalog because its parent stream '%s' is not accessible.",
                name, stream_cls.parent
            )
            schemas.pop(name, None)
            field_metadata.pop(name, None)

    if error_list:
        total_stream = len([stream for stream in STREAMS.values() if not stream.parent])
        streams_name = ", ".join(error_list)
        if len(error_list) != total_stream:
            message = "The account credentials supplied do not have 'read' access to the following stream(s): {}. "\
                "These streams have been excluded from the catalog.".format(streams_name)
            # If at least one stream has read permission, log a warning and continue with permitted streams only
            LOGGER.warning(message)
        else:
            message = "HTTP-error-code: 403, Error: The account credentials supplied do not have 'read' access to any "\
            "of streams supported by the tap. Data collection cannot be initiated due to lack of permissions."
            # If none of the streams have 'read' access, raise an error
            raise AftershipForbiddenError(message)

    return schemas, field_metadata
