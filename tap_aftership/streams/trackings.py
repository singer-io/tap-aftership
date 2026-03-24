from typing import Dict
from tap_aftership.streams.abstracts import IncrementalStream

class Trackings(IncrementalStream):
    tap_stream_id = "trackings"
    key_properties = ["id"]
    replication_method = "INCREMENTAL"
    replication_keys = ["updated_at"]
    data_key = "trackings"
    api_version = "2025-07"
    path = f"tracking/{api_version}/trackings"
    next_page_param = "cursor"
    next_page_key = "pagination.next_cursor"

    def update_params(self, state: Dict = None, parent_obj: Dict = None, **kwargs) -> None:
        """
        Update params for shipping streams with updated_at_min parameter
        """
        super().update_params(state=state, parent_obj=parent_obj, **kwargs)

        bookmark = self.get_bookmark(state or {}, self.tap_stream_id)
        self.params["updated_at_min"] = bookmark
