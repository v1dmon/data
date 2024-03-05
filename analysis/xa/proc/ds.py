from xa.io import src
from xa.proc import frame

import pandas as pd
from enum import Enum


class _general(Enum):
    drops = ["Type", "SubType"]
    dtypes = {"Timestamp": "datetime64[ns, UTC]", "TimeDelta": "float64"}


class network:
    general = _general


class _host(Enum):
    drops = ["Type", "SubType", "OperatingSystem", "OSType", "Architecture", "Name", "KernelVersion"]


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
    dtypes = {"Timestamp": "datetime64[ns, UTC]", "CPUPercUsage": "float64", "MemoryPercUsage": "float64"}


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
    dtypes = {"Timestamp": "datetime64[ns, UTC]", "Throughput": "float64", "Latency": "timedelta64[ns]"}
    renames = {"mean": "Latency", "requests": "Requests", "rate": "Rate", "throughput": "Throughput", "success": "Success"}


class http:
    result = _result
    metrics = _metrics


class Set:
    def __init__(self, lf: list[src.Log]) -> None:
        ng, sh, sn, sc, hr, hm = [], [], [], [], [], []

        for f in lf:
            for pl in f.content:
                t = pl["Type"]
                st = pl["SubType"]

                if t == "network":
                    if st == "general":
                        ng.append(pl)
                elif t == "structure":
                    if st == "host":
                        sh.append(pl)
                    elif st == "network":
                        sn.append(pl)
                    elif st == "container":
                        sc.append(pl)
                elif t == "http":
                    if st == "result":
                        hr.append(pl)
                    elif st == "metrics":
                        hm.append(pl)

        self.network = frame.Frame(general=ng)
        self.network.drop(general=network.general.drops.value)
        self.network.dtypes(general=network.general.dtypes.value)
        self.network.sortBy(general="Timestamp")

        self.structure = frame.Frame(host=sh, network=sn, container=sc)
        self.structure.normalize(container="Stats")
        self.structure.drop(host=structure.host.drops.value, network=structure.network.drops.value, container=structure.container.drops.value)
        self.structure.dtypes(container=structure.container.dtypes.value)
        self.structure.sortBy(host="Timestamp", network="Timestamp", container="Timestamp")

        self.http = frame.Frame(result=hr, metrics=hm)
        self.http.normalize(metrics="latencies")
        self.http.drop(result=http.result.drops.value, metrics=http.metrics.drops.value)
        self.http.rename(metrics=http.metrics.renames.value)
        self.http.dtypes(metrics=http.metrics.dtypes.value)
        self.http.sortBy(metrics="Timestamp")

        getattr(self.http, "metrics").Latency = getattr(self.http, "metrics").Latency.dt.total_seconds()
