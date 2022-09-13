"""Tables related to behavioral data.

During some recordings behavioral data is recorded.
This module organizes the different types of behavioral
raw data and relates them to the Recording.
"""

import datajoint as dj
from ..pipeline import session, event, db_prefix
from ..paths import get_experiment_root_data_dir
from ..ingest.harp import HarpLoader
from element_interface.utils import find_full_path

schema = dj.schema(db_prefix + "behavior")

__all__ = ["session", "db_prefix", "HarpDevice", "HarpRecording"]

# -------------- Table declarations --------------

# NOTE: Previous tables depreciated with the use of element-event


@schema
class HarpDevice(dj.Lookup):
    definition = """
    harp_device_id: int
    ---
    harp_device_name: varchar(36)
    harp_device_description='': varchar(1000)
    """

    contents = [(1, "example_a", "description")]


@schema
class HarpRecording(dj.Imported):
    definition = """
    -> event.BehaviorRecording
    -> HarpDevice
    """

    class Channel(dj.Part):
        definition = """
        -> master
        channel_name: varchar(36)
        ---
        data=null : longblob  # 1d array of acquired data for this channel
        time=null : longblob  # 1d array of timestamps for this channel 
        """

    def make(self, key):
        bpod_path_relative = (event.BehaviorRecording.File & key).fetch1("filepath")
        harp_paths = list(find_full_path(
            get_experiment_root_data_dir(), bpod_path_relative
        ).parent.glob("*harp*bin"))
        assert len(harp_paths) == 1, f"Found more than one harp file\n\t{harp_paths}"

        self.insert1(key)
        self.Channel.insert(
            [
                {**key, **channel} 
                for channel in HarpLoader(harp_paths[0]).data_for_insert()
            ]
        )
