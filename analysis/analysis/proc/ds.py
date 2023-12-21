from analysis.proc import fs
import pandas as pd


class Frame:
    def __init__(self, **kwargs) -> None:
        for key, data in kwargs.items():
            setattr(self, key, pd.DataFrame(data))

    def normalize(self, **kwargs):
        for key, col in kwargs.items():
            setattr(self, key, getattr(self, key).merge(pd.json_normalize(getattr(self, key)[col]), left_index=True, right_index=True))

    def drop(self, **kwargs):
        for key, cols in kwargs.items():
            getattr(self, key).drop(columns=cols, inplace=True, errors="ignore")


class DataSet:
    def __init__(self, logfiles: list[fs.LogFile]) -> None:
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

        self.network = Frame(general=networkGeneral)
        self.network.drop(general=["Type", "SubType"])

        self.structure = Frame(host=structureHost, network=structureNetwork, container=structureContainer)
        self.structure.normalize(container="Stats")
        self.structure.drop(
            host=[
                "Type",
                "SubType",
                "OperatingSystem",
                "OSType",
                "Architecture",
                "Name",
                "KernelVersion",
            ],
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

        self.http = Frame(result=httpResult, metrics=httpMetrics)
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
