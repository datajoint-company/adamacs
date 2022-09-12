"""Tables related to behavioral data.

During some recordings behavioral data is recorded.
This module organizes the different types of behavioral
raw data and relates them to the Recording.
"""

import datajoint as dj
from ..pipeline import session, db_prefix
from ..paths import get_harp_filepath
from ..ingest.harp import HarpLoader

schema = dj.schema(db_prefix + "behavior")

__all__ = [
    "session",
    "db_prefix",
    "HarpDevice",
    "HarpRecording"
]

# -------------- Table declarations --------------

# NOTE: Previous tables depreciated with the use of element-event

@schema
class HarpDevice(dj.Manual):
    definition = """
    harp_device_id: int
    ---
    harp_device_name: varchar(36)
    harp_device_description='': varchar(1000)
    """


@schema
class HarpRecording(dj.Imported):
    definition = """
    -> session.Session
    -> HarpDevice
    ---
    recording_duration=null: float  # duration (in seconds) of the harp acquisition 
    timestamps: longblob  # 1d array of timestamps (in seconds) of the acquired channel data
    """

    class Channel(dj.Part):
        definition = """
        -> master
        channel_id: int
        ---
        channel_name: varchar(36)
        trace: longblob  # 1d array of acquired data for this channel, same size as the "timestamps" array
        """

    def make(self, key):
        pass
        # aux_fp = get_harp_filepath(key)
        # loaded_aux = HarpLoader(aux_fp)

        # timestamps = loaded_aux.timestamps

        # channels = []
        # for aux_channel in loaded_aux.channels:
        #     trace = aux_channel.data
        #     assert len(trace) == len(timestamps)
        #     channels.append(
        #         {
        #             **key,
        #             "channel_id": aux_channel.id,
        #             "channel_name": aux_channel.name,
        #             "trace": trace,
        #         }
        #     )

        # self.insert1(
        #     {**key, "recording_duration": loaded_aux.duration, "timestamps": timestamps}
        # )
        # self.Channel.insert(channels)
