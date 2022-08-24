import numpy as np
from pywavesurfer import ws
from pathlib import Path
from element_interface.utils import find_full_path, find_root_directory
from ..paths import get_experiment_root_data_dir


class Auxfile(object):
    """Returns sets of timestamps by recording modality relative to aux file zero
    :property main_track_gate: main track gate start time
    :property shutter_timestamps: laser shutter
    :property mini2p_channels: dict of arrays for frame, line and volume
    :property cam_trigger: tracking camera trigger
    :property bpod_channels: dict of arrays for trial, reward and tone
    """

    def __init__(self, aux_path):
        self.aux_path = Path(aux_path)
        if not self.aux_path.exists():
            self._aux_path_full = find_full_path(
                get_experiment_root_data_dir(), aux_path
            )
        else:
            self._aux_path_full = Path(aux_path)
        self._aux_path_relative = self._aux_path_full.relative_to(
            find_root_directory(get_experiment_root_data_dir(), self._aux_path_full)
        )
        self._raw = ws.loadDataFile(
            filename=self._aux_path_full, format_string="double"
        )
        self._sweep = [x for x in self._raw.keys() if "sweep" in x][0]
        self._sample_rate = self._raw["header"]["AcquisitionSampleRate"][0][0]
        self._timebase = (
            np.arange(self._raw[self._sweep]["analogScans"].shape[1])
            / self._sample_rate
        )
        self._digital_channels = []
        self._gate = []
        self._shutter = []
        self._2p = {}
        self._cam = []
        self._bpod = {}

    @property
    def _digital(self, channels=5):  # this process could be time-consuming
        if len(self._digital_channels) == 0:
            auxdata = self._raw[self._sweep]["digitalScans"][0].flatten()
            binary = [[int(x) for x in f"{x:0{channels}b}"] for x in auxdata]
            self._digital_channels = np.array(binary, dtype=bool).T
        return self._digital_channels

    @property
    def main_track_gate(self):
        """Main track gate start time"""
        if not self._gate:
            self._gate = get_timestamps(self._digital[4], self._sample_rate)[0]
        return self._gate

    @property
    def shutter_timestamps(self):
        """Laser shutter"""
        if not any(self._shutter):
            self._shutter = get_timestamps(self._digital[3], self._sample_rate)
        return self._shutter

    @property
    def mini2p_channels(self):
        """Dict of arrays for frame, line and volume"""
        if not any(self._2p):
            self._2p = {  # vol and frame are the same in sample data
                "frame": get_timestamps(self._digital[2], self._sample_rate),
                "line": get_timestamps(self._digital[1], self._sample_rate),
                "volume": get_timestamps(self._digital[0], self._sample_rate),
            }
        return self._2p

    @property
    def cam_trigger(self):
        """Tracking camera trigger"""
        if not any(self._cam):
            self._cam = get_timestamps(
                self._raw[self._sweep]["analogScans"][0], self._sample_rate
            )
        return self._cam

    @property
    def bpod_channels(self):
        """Dict of arrays for trial, reward and tone"""
        # NOTE: In example aux, one reward pulse. BPod code registers more
        if not self._bpod:
            self._bpod = {
                "trial": get_timestamps(
                    self._raw[self._sweep]["analogScans"][1], self._sample_rate
                ),
                "reward": get_timestamps(
                    self._raw[self._sweep]["analogScans"][2], self._sample_rate
                ),
                "tone": get_timestamps(  # approx eq trial times with reqard times
                    self._raw[self._sweep]["analogScans"][3], self._sample_rate
                ),
            }
        return self._bpod


# --------------------- HELPER LOADER FUNCTIONS -----------------


def get_timestamps(data, sample_rate, threshold=1, rising_pulse=True):
    """Given data and sample rate, take vals above threshold and return rising times

    :param data (numpy array): Raw or analog signal from aux file
    :param sample_rate (float): acquistion sample rate from aux header
    :param threshold (float): Optional, default 1. If data is boolean, ignored.
    :param rising_pulse (bool): Optional, default True. Take even pulses from signal
                                If False, returns all available timestamps
    :returns timestamps (nump array)
    """
    if data.dtype == "bool":
        data = data > 0.5
    else:
        data = data > threshold

    timestamps = np.argwhere(np.diff(data) != 0)[:, 0] / sample_rate

    if rising_pulse:
        return timestamps[::2]  # take even items (rising pulse)
    else:
        return timestamps
