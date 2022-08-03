## NEEDS FIXING - how does subclass refer to parent class?

import logging
from pathlib import Path
import scipy.io as spio
import numpy as np
from dateutil import parser
from element_interface.utils import find_full_path
from ..pipeline import trial, event
from ..paths import get_experiment_root_data_dir

logger = logging.getLogger("datajoint")


class BPodFile:
    def __init__(self, bpod_path):
        self.bpod_path = Path(bpod_path)
        if not self.bpod_path.exists():
            bpod_path_full = find_full_path(get_experiment_root_data_dir(), bpod_path)
        else:
            bpod_path_full = Path(bpod_path)

        # NOTE: Daniel made a comment that np.squeeze did work on singleton dimensions
        #       returning empty array. Chris couldn't find the same issue
        self._raw_data = spio.loadmat(bpod_path_full, simplify_cells=True)

    @property
    def start_time(self):  # bpod file creation time in UTC
        return parser.parse(
            str(self._raw_data["__header__"]).split("Created on:")[-1][1:-1]
        )

    @property
    def session_data(self):
        return self._raw_data["SessionData"]

    @property
    def bpod_version(self):
        return self.session_data["Info"]["StateMachineVersion"].split(" ")[-1]

    @property
    def recording_duration(self):
        return sum(
            self.session_data["TrialEndTimestamp"]
            - self.session_data["TrialStartTimestamp"]
        )

    @property
    def n_trials(self):
        return self.session_data["nTrials"]

    @property
    def trial_data(self):
        return self.session_data["RawEvents"]["Trial"]

    class Trial:
        def __init__(self, idx):
            self._idx = idx
            self._parent = UNKNOWN  # TODO: figure out calling parent

        @property
        def name(self):
            return self._parent.session_data["TrialTypeNames"][self._idx]

        @property
        def start(self):
            return self._parent.session_data["TrialStartTimestamp"][self._idx]

        @property
        def end(self):
            return self._parent.session_data["TrialEndTimestamp"][self._idx]

        @property
        def states(self):
            states_dict = self._parent.trial_data[self._idx]["States"]
            # Filter out states with all nan values:
            return {k: v for k, v in states_dict.items() if not np.all(np.isnan(v))}

        @property
        def events(self):
            return self._parent.trial_data[self._idx]["Events"]

        @property
        def time_to_port(self):
            return self.states.get("WaitForResponse")

        @property
        def cue_delay(self):
            return self.states.get("CueDelay")

        @property
        def drinking(self):
            return self.states.get("Drinking")

        @property
        def reward(self):  # following beacon_pokes_plot.m, only first trial
            return (
                self.time_to_port
                + self.session_data["TrialSettings"][0]["GUI"]["RewardDelay"]
            )

        @property  # NOTE: assumes one port in event per trial
        def port_in(self):
            """Returns number and timestamp of input port"""
            ports_in = [port for port in self.events if "In" in port]
            assert len(ports_in) == 1, (
                "Code assumes only one port-in event per trial.\n"
                + f"Please refactor and test with {self.bpod_path.stem}"
            )
            return ports_in[0][4:-2], self.events[ports_in[0]]

        @property
        def error(self):
            return True if "Punish" in self.states else False


# --------------------- HELPER LOADER FUNCTIONS -----------------


# matlab script exact translation. Makes tuple: for any port with 'in'.
# Not needed abov e
def PortInEvents(bpod_session, idx):
    """Replicate MATLAB func: return list of tuples for input ports: #, events, name"""
    events = bpod_session["RawEvents"]["Trial"][idx]["Events"]
    in_ports = [f for f in events.keys() if "In" in f]
    in_port_events = []
    for port in in_ports:
        # (port#, event times, portname)
        in_port_events.append((port[4:-2], events[port], port))
    return in_port_events
