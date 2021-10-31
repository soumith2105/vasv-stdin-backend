from enum import Enum


class SignupStatusCodes(Enum):
    SUCCESS = "SIGNUP__SUCCESS"
    NOT_YET_STARTED = "SIGNUP__NOT_YET_STARTED"
    IN_PROGRESS = "SIGNUP__IN_PROGRESS"
    FAILED = "SIGNUP__FAILED"


class FailedSyncStatusCodes(Enum):
    RESULT_SYNC = "FAILED__RESULT_SYNC"
    ATTENDANCE_SYNC = "FAILED__ATTENDANCE_SYNC"
    SYNC = "FAILED__SYNC_CORRUPT"


class SyncStatusCodes(Enum):
    ATTENDANCE_SYNC = "ATTENDANCE_SYNC"
    RESULT_SYNC = "RESULT_SYNC"
    IN_PROGRESS = "SYNC__IN_PROGRESS"
    COMPLETE = "SYNC__COMPLETE"
