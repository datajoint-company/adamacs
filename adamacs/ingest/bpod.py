import logging
import numpy as np
import datajoint as dj
import scipy.io as spio
from pathlib import Path
from dateutil import parser
from element_interface.utils import find_full_path
from ..pipeline import trial, event, session
from ..paths import get_experiment_root_data_dir

logger = logging.getLogger("datajoint")


class Bpodfile(object):
    def __init__(self, bpod_path):
        self.bpod_path = Path(bpod_path)
        if not self.bpod_path.exists():
            self._bpod_path_full = find_full_path(
                get_experiment_root_data_dir(), bpod_path
            )
        else:
            self._bpod_path_full = Path(bpod_path)

        # NOTE: Daniel made a comment that np.squeeze did work on singleton dimensions
        #       returning empty array. Chris couldn't find the same issue
        self._raw_data = spio.loadmat(self._bpod_path_full, simplify_cells=True)

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
    def recording_duration(self):  # In seconds
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

    def trial(self, idx):
        return Trial(idx, self._bpod_path_full, self.session_data, self.trial_data)

    def ingest(self):
        session_key = {
            "session_id": (
                dj.U().aggr(session.Session, n="max(session_id)").fetch("n") or 0
            )
            + 1,  # incriment previous session id by 1
            "subject": self.session_data["CurrentSubjectName"],
            "session_datetime": self.start_time,
        }

        with session.Session.connection.transaction:
            session.insert1(session_key)
            # event.insert()
            # trial.insert()


class Trial(object):
    def __init__(self, idx, bpod_path_full, session_data=None, trial_data=None):
        if not session_data:
            session_data = Bpodfile(bpod_path_full).session_data
        if not trial_data:
            trial_data = Bpodfile(bpod_path_full).trial_data
        self._idx = idx
        self._bpod_path_full = bpod_path_full
        self._session_data = session_data
        self._trial_data = trial_data

    @property
    def name(self):
        return self._session_data["TrialTypeNames"][self._idx]

    @property
    def start(self):
        return self._session_data["TrialStartTimestamp"][self._idx]

    @property
    def end(self):
        return self._session_data["TrialEndTimestamp"][self._idx]

    @property
    def states(self):
        states_dict = self._trial_data[self._idx]["States"]
        # Filter out states with all nan values:
        return {k: v for k, v in states_dict.items() if not np.all(np.isnan(v))}

    @property
    def events(self):
        return self._trial_data[self._idx]["Events"]

    @property
    def _time_to_list(self):
        return self.states.get("WaitForResponse")

    @property
    def time_to_port(self):
        if len(self._time_to_list) > 1:  # Sometimes this is None
            return self._time_to_list[1] - self._time_to_list[0]

    @property
    def time_to_target(self):
        return self._time_to_list[0] if self._time_to_list else None

    @property
    def cue_delay(self):  # first item is 'Trigger Zone entry'. Ignore second?
        # Below, [None] avoids TypeErr if no CueDelay
        return self.states.get("CueDelay", [None])[0]

    @property
    def drinking(self):
        return self.states.get("Drinking")

    @property
    def reward(self):  # following beacon_pokes_plot.m, only first trial
        return (
            self.time_to_port
            + self._session_data["TrialSettings"][0]["GUI"]["RewardDelay"]
        )

    @property  # TODO: Can we assume one port_in event per trial?
    def port_in(self):
        """Returns list of tuples: number and timestamp of input port"""
        ports_in = [  # tuple of port# and timestamp
            (int(port[4:-2]), self.events[port]) for port in self.events if "In" in port
        ]
        return ports_in if ports_in else None

    @property
    def error(self):
        return True if "Punish" in self.states else False

    @property
    def timeout(self):
        return (
            True
            if self.time_to_port
            >= self._session_data["TrialSettings"][self._idx]["GUI"]["ResponseTime"]
            else False
        )


# --------------------- HELPER LOADER FUNCTIONS -----------------

# matlab script exact translation by request
# Depreciated by Trial.port_in above
def PortInEvents(bpod_session, idx):
    """Replicate MATLAB func: return list of tuples for input ports: #, events, name"""
    events = bpod_session["RawEvents"]["Trial"][idx]["Events"]
    in_ports = [f for f in events.keys() if "In" in f]
    in_port_events = []
    for port in in_ports:
        # (port#, event times, portname)
        in_port_events.append((port[4:-2], events[port], port))
    return in_port_events
