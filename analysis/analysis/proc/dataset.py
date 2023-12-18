from analysis.io import logfile
from analysis.proc import frame
import pandas as pd


class DataSet:
    def __init__(self, logfiles: list[logfile.LogFile]) -> None:
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
        self.network.drop(general=["Type", "SubType"])
        self.network.dtypes(general={"Timestamp": "datetime64[ns, UTC]", "TimeDelta": "float64"})
        self.network.sortby(general="Timestamp")

        self.structure = frame.Frame(host=structureHost, network=structureNetwork, container=structureContainer)
        self.structure.normalize(container="Stats")
        self.structure.drop(
            host=["Type", "SubType", "OperatingSystem", "OSType", "Architecture", "Name", "KernelVersion"],
            network=["Type", "SubType", "ID"],
            container=[
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
            ],
        )
        self.structure.dtypes(container={"Timestamp": "datetime64[ns, UTC]", "CPUPercUsage": "float64", "MemoryPercUsage": "float64"})
        self.structure.sortby(host="Timestamp", network="Timestamp", container="Timestamp")

        self.http = frame.Frame(result=httpResult, metrics=httpMetrics)
        self.http.normalize(metrics="latencies")
        self.http.drop(
            # TODO select columns to drop in http.result
            result=["Type", "SubType"],
            metrics=[
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
            ],
        )
        self.http.rename(metrics={"mean": "Latency", "requests": "Requests", "rate": "Rate", "throughput": "Throughput", "success": "Success"})
        self.http.dtypes(metrics={"Timestamp": "datetime64[ns, UTC]", "Throughput": "float64", "Latency": "int64"})
        self.http.sortby(metrics="Timestamp")


class MetricSet:
    def __init__(self, data: DataSet) -> None:
        om = getattr(data.network, "general")
        self.timedelta = om[["Timestamp", "TimeDelta"]]

        om = getattr(data.structure, "container")
        self.cpuUsage = om[["Timestamp", "CPUPercUsage"]]
        self.memoryUsage = om[["Timestamp", "MemoryPercUsage"]]

        # TODO get latencies from http.result
        # WARN enable http.result by default in experiments
        om = getattr(data.http, "result")
        if om.empty:
            om = getattr(data.http, "metrics")
        self.latency = om[["Timestamp", "Latency"]]

        om = getattr(data.http, "metrics")
        self.throughput = om[["Timestamp", "Throughput"]]
