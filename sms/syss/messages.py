"""Define message templates."""

# Official Libraries


def _with_data(text: str) -> str:
    assert isinstance(text, str)

    return text + ': %s'


# Process messages
PROC_START = '> Starting {proc} ...'

PROC_SUCCESS = '___{proc} Successfull.'

PROC_DONE = '... {proc} ...DONE.'

PROC_DONE_WITH_DATA = _with_data(PROC_DONE)

PROC_INITIALIZED = '... {proc} Initialized.'

PROC_MESSAGE = '... {proc}.'

PROC_MESSAGE_WITH_DATA = _with_data(PROC_MESSAGE)


# General messages
MSG_UNIMPLEMENT_PROC = '>> unimplement {proc} <<'


# Error messages
ERR_FAIL_PROC = '! Failed {proc}!'

ERR_FAIL_PROC_WITH_DATA = _with_data(ERR_FAIL_PROC)

ERR_FAIL_CANNOT_CREATE_DATA = '! Failed. Cannot create {data}!'

ERR_FAIL_CANNOT_CREATE_DATA_WITH_DATA = _with_data(ERR_FAIL_CANNOT_CREATE_DATA)

ERR_FAIL_CANNOT_INITIALIZE = '! Failed. Cannot initialize {data}!'

ERR_FAIL_CANNOT_INITIALIZE_WITH_DATA = _with_data(ERR_FAIL_CANNOT_INITIALIZE)

ERR_FAIL_CANNOT_REMOVE_DATA = '! Failed Cannot remove {data}!'

ERR_FAIL_CANNOT_REMOVE_DATA_WITH_DATA = _with_data(ERR_FAIL_CANNOT_REMOVE_DATA)

ERR_FAIL_CANNOT_WRITE_DATA = '! Failed Cannot write {data}!'

ERR_FAIL_CANNOT_WRITE_DATA_WITH_DATA = _with_data(ERR_FAIL_CANNOT_WRITE_DATA)

ERR_FAIL_DUPLICATED_DATA = '! Failed. Duplicated {data}!'

ERR_FAIL_DUPLICATED_DATA_WITH_DATA = _with_data(ERR_FAIL_DUPLICATED_DATA)

ERR_FAIL_INVALID_DATA = '! Failed Invalid {data}!'

ERR_FAIL_INVALID_DATA_WITH_DATA = _with_data(ERR_FAIL_INVALID_DATA)

ERR_FAIL_MUSTBE = '! Failed Must be {data}!'

ERR_FAIL_MUSTBE_WITH_DATA = _with_data(ERR_FAIL_MUSTBE)

ERR_FAIL_MISSING_DATA = '! Failed. Missing {data}!'

ERR_FAIL_MISSING_DATA_WITH_DATA = _with_data(ERR_FAIL_MISSING_DATA)

ERR_FAIL_SUBPROCESS = '! Failed Subprocess of {proc}!'

ERR_FAIL_SUBPROCESS_WITH_DATA = _with_data(ERR_FAIL_SUBPROCESS)

ERR_FAIL_UNKNOWN_DATA = '! Failed. Unknown {data}!'

ERR_FAIL_UNKNOWN_DATA_WITH_DATA = _with_data(ERR_FAIL_UNKNOWN_DATA)
