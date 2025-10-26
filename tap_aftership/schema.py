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
                if response.get("meta", {}).get("code") != 200:
                    raise AftershipForbiddenError
        except AftershipForbiddenError:
            error_list.append(stream_name)
            if stream_obj.children:
                error_list.extend(stream_obj.children)

    if error_list:
        total_stream = len(STREAMS.values())
        streams_name = ", ".join(error_list)
        if len(error_list) != total_stream:
            message = "The account credentials supplied do not have 'read' access to the following stream(s): {}. "\
                "The data for these streams would not be collected due to lack of required permission.".format(streams_name)
            # If atleast one stream have read permission then just print warning message for all streams
            # which does not have read permission
            LOGGER.warning(message)
        else:
            message ="HTTP-error-code: 403, Error: The account credentials supplied do not have 'read' access to any "\
            "of streams supported by the tap. Data collection cannot be initiated due to lack of permissions."
            # If none of the streams are having the 'read' access, then the code will raise an error
            raise AftershipForbiddenError(message)

    return schemas, field_metadata
