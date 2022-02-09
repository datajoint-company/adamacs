
from pathlib import Path
import scipy.io as spio
import datajoint as dj
from element_interface import find_full_path
from adamacs import db_prefix, behavior
from adamacs.paths import get_bpod_root_data_dir, get_session_dir

schema = dj.schema(db_prefix + 'bpod_ingest')


@schema
class BehaviorIngest(dj.Imported):
    definition = """
    -> session.Recording
    """

    def make(self, key):  # reading bpod data to populate
        # could model dir navigation after element_array_ephys
        # which uses config file for root dir and csv for relative paths
        # https://github.com/datajoint/workflow-array-ephys/blob/main/workflow_array_ephys/paths.py
        bpod_root_dir = Path(get_bpod_root_data_dir(key))
        bpod_sess_dir = Path(get_session_dir(key))
        bpod_dir = find_full_path(bpod_root_dir, bpod_sess_dir)

        bpod_filepath = next(bpod_dir.glob('*.mat'))
        trial_info = load_bpod_matfile(key, bpod_filepath)
        behavior.Trial.insert(trial_info, ignore_extra_fields=True)
        behavior.Event.insert(trial_info, ignore_extra_fields=True)

# --------------------- HELPER LOADER FUNCTIONS -----------------

# see full example here:
# https://github.com/mesoscale-activity-map/map-ephys/blob/master/pipeline/ingest/behavior.py


def load_bpod_matfile(key, matlab_filepath):
    """
    Loading routine for behavioral file, bpod .mat
    """
    # Loading the file
    SessionData = spio.loadmat(matlab_filepath.as_posix(),
                               squeeze_me=True, struct_as_record=False
                               )['SessionData']
    return SessionData

# Add to dict for insertion. For example:
# for trial in range(SessionData.nTrials):
#     trial_info['start_time'] = SessionData.RawData.OriginalEventTimestamps[trial]
# return trial_info


''' NOTES on bpod example file:
bpod SessionData structure
    TrialTypes - 1,2,3,1,2,3
    TrialTypeNames - Visibile,Visible,Fading
    Info
        StateMachineVersion
        SessionDate
        SessionStartTime_UTC
        SessionStartTime_MATLAB
    nTrials (# trials in session, here 54)
    RawEvents (timestamps for each trial's state transitions/recorded events)
        Trial{1,n}.States #Which of these are important?
            WaitForPosTriggerSoftCode
            CueDelay
            WaitForResponse
            Port2RewardDelay
            Port2Reward
            CloseValves
            Drinking
            Port1RewardDelay
            Port3RewardDelay
            Port4RewardDelay
            Port5RewardDelay
            Port6RewardDelay
            Port7RewardDelay
            Port8RewardDelay
            Port1Reward
            Port3Reward
            Port4Reward
            Port5Reward
            Port6Reward
            Port7Reward
            Port8Reward
            Punish
            Punishexit
            EarlyWithdrawal
        Trial{1,n}.Events
            Port4In
            Port4Out
            SoftCode10
            Tup
            Port2In
            Port2Out
    RawData (copy of raw data from state machine)
    TrialStartTimestamp (time when trial started on Bpod's clock)
        Note: Timestamps in RawEvents are relative to each trial's start
    TrialEndTimestamp
    SettingsFile (the settings file you selected in the launch manager)
    Notes
    MarkerCodes
    CurrentSubjectName
    TrialSettings
        GUI
        GUIMeta
        GUIPanels
        polling
        debug
        debugvis
        Data
        arm_number
        arm_baited_orig
        arm_baited
        SF
        rotation
        position
        StimAlpha
    StimPos
        TriggerLocPix
        TriggerLocOptitrackHitbox
        TriggerLocOptitrackCenter
        TriggerLocOptitrackCircleHitRadius
        tform
'''
