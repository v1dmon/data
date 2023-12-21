from xa.io import src
from xa.proc import frame

import pandas as pd
from enum import Enum


class _general(Enum):
    drops = ["Type", "SubType"]
    dtypes = {
        "Timestamp": "datetime64[ns, UTC]",
        "TimeDelta": "float64",
    }


class network:
    general = _general


class _host(Enum):
    drops = [
        "Type",
        "SubType",
        "OperatingSystem",
        "OSType",
        "Architecture",
        "Name",
        "KernelVersion",
    ]


class _network(Enum):
    drops = ["Type", "SubType", "ID"]


class _container(Enum):
    drops = [
        "Type",
        "SubType",
        "ID",
        "Image",
        "Locale",
        "Timezone",
        "IPAddresses",
        "Ports",
        "Stats",
        "CPURawUsage",
        "CPUSystemRawUsage",
        "CPUOnline",
        "MemoryRawLimit",
        "MemoryRawUsage",
        "NetworkRxRaw",
        "NetworkTxRaw",
        "BlockIORawRead",
        "BlockIORawWrite",
        "PIDsCurrent",
        "PIDsLimit",
    ]
    dtypes = {
        "Timestamp": "datetime64[ns, UTC]",
        "CPUPercUsage": "float64",
        "MemoryPercUsage": "float64",
    }


class structure:
    host = _host
    network = _network
    container = _container


class _result(Enum):
    drops = ["Type", "SubType"]


class _metrics(Enum):
    drops = [
        "Type",
        "SubType",
        "bytes_in",
        "bytes_out",
        "earliest",
        "latest",
        "end",
        "duration",
        "wait",
        "latencies",
        "total",
        "50th",
        "90th",
        "95th",
        "99th",
        "max",
        "min",
    ]
    dtypes = {
        "Timestamp": "datetime64[ns, UTC]",
        "Throughput": "float64",
        "Latency": "int64",
    }
    renames = {
        "mean": "Latency",
        "requests": "Requests",
        "rate": "Rate",
        "throughput": "Throughput",
        "success": "Success",
    }


class http:
    result = _result
    metrics = _metrics


class Set:
    def __init__(self, logfiles: list[src.Log]) -> None:
        networkGeneral = []
        structureHost = []
        structureNetwork = []
        structureContainer = []
        httpResult = []
        httpMetrics = []

        for log in logfiles:
            for payload in log.content:
                type = payload["Type"]
                subtype = payload["SubType"]

                if type == "network":
                    if subtype == "general":
                        networkGeneral.append(payload)
                elif type == "structure":
                    if subtype == "host":
                        structureHost.append(payload)
                    elif subtype == "network":
                        structureNetwork.append(payload)
                    elif subtype == "container":
                        structureContainer.append(payload)
                elif type == "http":
                    if subtype == "result":
                        httpResult.append(payload)
                    elif subtype == "metrics":
                        httpMetrics.append(payload)

        self.network = frame.Frame(general=networkGeneral)
        self.network.drop(general=network.general.drops.value)
        self.network.dtypes(general=network.general.dtypes.value)
        self.network.sortBy(general="Timestamp")

        self.structure = frame.Frame(
            host=structureHost,
            network=structureNetwork,
            container=structureContainer,
        )
        self.structure.normalize(container="Stats")
        self.structure.drop(
            host=structure.host.drops.value,
            network=structure.network.drops.value,
            container=structure.container.drops.value,
        )
        self.structure.dtypes(container=structure.container.dtypes.value)
        self.structure.sortBy(host="Timestamp", network="Timestamp", container="Timestamp")

        self.http = frame.Frame(result=httpResult, metrics=httpMetrics)
        self.http.normalize(metrics="latencies")
        self.http.drop(result=http.result.drops.value, metrics=http.metrics.drops.value)
        self.http.rename(metrics=http.metrics.renames.value)
        self.http.dtypes(metrics=http.metrics.dtypes.value)
        self.http.sortBy(metrics="Timestamp")
