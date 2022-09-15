import numpy as np
import datajoint as dj
import scipy.io as spio
from pathlib import Path
from bisect import bisect
from dateutil import parser
from element_interface.utils import find_full_path, find_root_directory
from ..pipeline import subject, session, trial, event
from ..paths import get_experiment_root_data_dir
from .aux import Auxfile


class Bpodfile(object):
    def __init__(self, bpod_path):
        self.bpod_path = Path(bpod_path)
        if not self.bpod_path.exists():
            self._bpod_path_full = find_full_path(
                get_experiment_root_data_dir(), bpod_path
            )
        else:
            self._bpod_path_full = Path(bpod_path)
        self._bpod_path_relative = self._bpod_path_full.relative_to(
            find_root_directory(get_experiment_root_data_dir(), self._bpod_path_full)
        )

        # NOTE: Daniel made a comment that np.squeeze didn't work on singleton
        #       dimensions, returning empty array. Chris couldn't find the same issue
        self._raw_data = spio.loadmat(self._bpod_path_full, simplify_cells=True)

        self._trials = {}  # dict to be loaded with all trials accessed
        self.session_data = self._raw_data["SessionData"]
        self.trial_data = self.session_data["RawEvents"]["Trial"]
        self.n_trials = self.session_data["nTrials"]
        self.subject_id = self.session_data["CurrentSubjectName"]
        self.start_time = parser.parse(
            self.session_data["Info"]["SessionDate"]  # format: 18-Mar-2022
            + " "
            + self.session_data["Info"]["SessionStartTime_UTC"]  # format: 16:55:28
        )

    @property
    def trials(self):
        """Loads all trials for this file into memory"""
        [self.trial(idx) for idx in range(self.n_trials)]
        return self._trials

    def trial(self, idx):
        """Loads a specific trial into memory using the trial index"""
        if idx not in self._trials:
            self._trials[idx] = Trial(
                idx, self._bpod_path_full, self.session_data, self.trial_data
            )
        return self._trials[idx]

    def _aux_timestamps(self):
        aux_paths = list(self._bpod_path_full.parent.glob("*h5"))
        assert len(aux_paths) == 1, f"Found more than one Aux h5 file\n{aux_paths}"
        aux = Auxfile(aux_paths[0])
        aux_onset = aux.main_track_gate  # master trigger
        aux_trials = aux.bpod_channels["trial"] - aux_onset  # trial times wrt trigger
        aux_rewards = aux.bpod_channels["reward"] - aux_onset  # rewards wrt trigger
        assert len(aux_trials) == self.n_trials, (
            "Number of trials do not match: "
            + f"BPod {self.n_trials} vs. Aux {len(aux_trials)}"
        )
        return aux_trials, aux_rewards

    def ingest(self, prompt=True):
        """Ingest BPod data to session, event, and trial tables.

        :param prompt (bool): Optional, default True. Prompt with metadata before entry.
        """
        # -------------------------- Check if already exists --------------------------
        if event.BehaviorRecording.File & f"filepath='{self._bpod_path_relative}'":
            print("Session already exists, skipping...")  # check this bpod file path
            return
        if not subject.Subject & f'subject="{self.subject_id}"':  # check this subject
            from .pyrat import PyratIngestion

            print(
                f"Subject does not yet exist."
                + f"Attempting pyrat import: {self.subject_id}"
            )
            PyratIngestion().ingest_animal(self.subject_id)

        # ------------------------------- Some constants -------------------------------
        session_id = (  # incriment previous session id by 1
            dj.U().aggr(session.Session, n="max(session_id)").fetch("n") or 0
        ) + 1
        bpod_version = self.session_data["Info"]["StateMachineVersion"].split(" ")[-1]
        aux_trials, aux_rewards = self._aux_timestamps()

        # ------------------------------- Keys to insert -------------------------------
        session_key = {
            "session_id": session_id,
            "subject": self.subject_id,
            "session_datetime": self.start_time,
        }
        behavior_recording_key = {
            "session_id": session_id,
            "recording_start_time": self.start_time,
            "recording_duration": sum(
                # removes time between trials, following example matlab code
                self.session_data["TrialEndTimestamp"]
                - self.session_data["TrialStartTimestamp"]
            ),
            "recording_notes": f"BPod version: {bpod_version}",
        }
        behavior_recording_fp_key = {
            "session_id": session_id,
            "filepath": self._bpod_path_relative,
        }
        trial_type_keys = [
            {
                "trial_type": trial_type
                for trial_type in np.unique(
                    self.session_data["TrialTypeNames"]
                ).tolist()
            }
        ]
        trial_keys = [
            {
                "session_id": session_id,
                "trial_id": n,
                "trial_type": self.trial(n).type,
                "trial_start_time": aux_trials[n],
                "trial_stop_time": aux_trials[n] + self.trial(n).duration,
            }
            for n in range(self.n_trials)
        ]
        trial_attributes_keys = [
            {
                "session_id": session_id,
                "trial_id": n,
                "attribute_name": attrib,
                "attribute_value": self.trial(n).attributes[attrib],
            }
            for n in range(self.n_trials)
            for attrib in self.trial(n).attributes
            if self.trial(n).attributes[attrib]
        ]
        event_type_keys = [
            {"event_type": event_type}
            for event_type in set(
                event_type
                for n in range(self.n_trials)
                for event_type in self.trial(n).events
            )
        ]
        event_keys = [
            {
                "session_id": session_id,
                "trial_id": n,
                "event_type": event,
                "event_start_time": aux_trials[n] + event_start,
            }
            for n in range(self.n_trials)
            for event, event_start in self.trial(n).events.items()
            if event_start
        ]
        event_keys.extend(
            [  # add reward times from aux
                {
                    "session_id": session_id,
                    "trial_id": bisect(aux_trials, reward) - 1,  # finds trial ID
                    "event_type": "reward",
                    "event_start_time": reward,
                }
                for reward in aux_rewards
            ]
        )

        # ---------------------------------- Prompt ----------------------------------
        print(
            "\n\t".join(
                [
                    "BPod items to be inserted:",
                    f"Subject : {self.subject_id}",
                    f"Time    : {self.start_time}",
                    f"N Trials: {self.n_trials}",
                    f"N Events: {len(event_keys)}",
                ]
            )
        )
        if (
            prompt
            and dj.utils.user_choice("Proceed with new subject(s) insert?") != "yes"
        ):
            print("Canceled insert.")
            return

        # ----------------------------- Insert to schemas -----------------------------
        with session.Session.connection.transaction:
            session.Session.insert1(session_key, skip_duplicates=True)  # remove skip
            event.BehaviorRecording.insert1(behavior_recording_key)
            event.BehaviorRecording.File.insert1(behavior_recording_fp_key)
            trial.TrialType.insert(trial_type_keys, skip_duplicates=True)
            trial.Trial.insert(trial_keys, allow_direct_insert=True)
            trial.Trial.Attribute.insert(
                trial_attributes_keys, allow_direct_insert=True
            )
            event.EventType.insert(event_type_keys, skip_duplicates=True)
            event.Event.insert(
                event_keys, allow_direct_insert=True, ignore_extra_fields=True
            )  # ignore extra trial_id
            trial.TrialEvent.insert(event_keys, allow_direct_insert=True)


class Trial(object):
    def __init__(self, idx, bpod_path_full, session_data=None, trial_data=None):
        if not session_data:
            session_data = Bpodfile(bpod_path_full).session_data
        if not trial_data:
            trial_data = Bpodfile(bpod_path_full).trial_data

        # -- properties --
        # for args above
        self._idx = idx
        self._bpod_path_full = bpod_path_full
        self._session_data = session_data
        self._trial_data = trial_data
        # for general use
        self.type = self._session_data["TrialTypeNames"][self._idx]
        self.duration = (  # endtime - start time. Will use Aux start time above
            self._session_data["TrialEndTimestamp"][self._idx]
            - self._session_data["TrialStartTimestamp"][self._idx]
        )
        # lazy loading
        self._attributes = {}
        self._events = {}

        # clean up bpod states
        self._states = {
            k: v
            for k, v in self._trial_data[self._idx]["States"].items()
            # Filter out states with nan values:
            if not np.any(np.isnan(v))
        }  # [None] below makes it easier to differentiate values from returned None
        self._resp_delay = self._states.get("WaitForResponse", [None])
        if self._resp_delay[0] and np.isnan(self._resp_delay[0]):
            self._resp_delay = [None]  # sometimes _resp_delay is [nan, nan]
        self._time_to_port = (
            self._resp_delay[1] - self._resp_delay[0] if self._resp_delay[0] else None
        )

        # clean up bpod port events
        self._raw_events = self._trial_data[self._idx]["Events"]
        self._ports_in = {
            f"in_port_{port[4:-2]}": self._raw_events[port]  # e.g., in_port_2: 8.3
            for port in self._raw_events
            if "In" in port
        }

    @property
    def attributes(self):
        """Returns all attributes for trial.Trial.Attributes as a dict"""
        if not self._attributes:
            self._attributes = {
                "error": True if "Punish" in self._states else False,
                "timeout": (
                    True
                    if self._time_to_port
                    and self._time_to_port
                    >= self._session_data["TrialSettings"][self._idx]["GUI"][
                        "ResponseTime"
                    ]
                    else False
                ),
            }
        return self._attributes

    @property
    def events(self):
        """Returns trial events as a dict {event_type: event_time} WRT trial start"""
        if not self._events:
            self._events = {
                "cue": self._states.get("CueDelay", [None])[0],
                "at_target": self._resp_delay[0] if self._resp_delay[0] else None,
                "at_port": self._time_to_port,
                # "reward": (
                #     # NOTE: Now taking reward events from Aux
                #     self._time_to_port
                #     + self._session_data["TrialSettings"][0]["GUI"]["RewardDelay"]
                #     if self._time_to_port
                #     else None
                # ),
                **self._ports_in,
                "drinking": self._states.get("Drinking", [None])[0],
            }
        return self._events


# --------------------- HELPER LOADER FUNCTIONS -----------------

# matlab script exact translation
# Depreciated by Trial attribute/event split above: port_num vs at_port time
def PortInEvents(bpod_session, idx):
    """Replicate MATLAB func: return list of tuples for input ports: #, events, name"""
    events = bpod_session["RawEvents"]["Trial"][idx]["Events"]
    in_ports = [f for f in events.keys() if "In" in f]
    in_port_raw_events = []
    for port in in_ports:
        # (port#, event times, portname)
        in_port_raw_events.append((port[4:-2], events[port], port))
    return in_port_raw_events
