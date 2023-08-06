import enum as _enum
import typing as _typing


class ArchiverSamplingMethod(str, _enum.Enum):
    MONITOR = "MONITOR"
    SCAN = "SCAN"


class ArchiverDisconnectedPV(_typing.NamedTuple):
    command_thread_id: str
    connection_lost_at: str
    extras: dict
    host_name: str
    instance: str
    internal_state: str
    last_known_event: str
    no_connection_as_of_epoch_secs: str
    pv_name: str


def _make_archiver_disconnected_pv(
    commandThreadID,
    connectionLostAt,
    hostName,
    instance,
    internalState,
    lastKnownEvent,
    noConnectionAsOfEpochSecs,
    pvName,
    **extras,
) -> ArchiverDisconnectedPV:
    return ArchiverDisconnectedPV(
        command_thread_id=commandThreadID,
        connection_lost_at=connectionLostAt,
        extras=extras,
        host_name=hostName,
        instance=instance,
        internal_state=internalState,
        last_known_event=lastKnownEvent,
        no_connection_as_of_epoch_secs=noConnectionAsOfEpochSecs,
        pv_name=pvName,
    )


class ArchiverPausedPV(_typing.NamedTuple):
    pv_name: str
    instance: str
    modification_time: str


def _make_archiver_paused_pv(pvName, instance, modificationTime, **extras):
    return ArchiverPausedPV(
        pv_name=pvName, instance=instance, modification_time=modificationTime
    )


class ArchiverStatusPVExtras(_typing.NamedTuple):
    appliance: str
    connection_first_established: str
    connection_last_restablished: str
    connection_loss_regain_count: str
    connection_state: str
    is_monitored: str
    last_event: str
    last_rotate_logs: str
    pv_name_only: str
    sampling_period: str


class ArchiverStatusPV(_typing.NamedTuple):
    pv_name: str
    status: str
    extras: _typing.Optional[ArchiverStatusPVExtras]


class ArchiverDroppedByTypeChangePV(_typing.NamedTuple):
    events_dropped: str
    pv_name: str


class ArchiverGenericReponse(_typing.NamedTuple):
    success: bool
    status_code: int
    text: str
    json: _typing.Optional[_typing.Union[list, dict]]


def _make_archiver_status_pv(pvName: str, status: str, **extras):
    return ArchiverStatusPV(
        pv_name=pvName,
        status=status,
        extras=None
        if not extras
        else ArchiverStatusPVExtras(
            appliance=extras["appliance"],
            connection_first_established=extras["connectionFirstEstablished"],
            connection_last_restablished=extras["connectionLastRestablished"],
            connection_loss_regain_count=extras["connectionLossRegainCount"],
            connection_state=extras["connectionState"],
            is_monitored=extras["isMonitored"],
            last_event=extras["lastEvent"],
            last_rotate_logs=extras["lastRotateLogs"],
            pv_name_only=extras["pvNameOnly"],
            sampling_period=extras["samplingPeriod"],
        ),
    )
