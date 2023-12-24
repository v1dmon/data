from xa.proc import ds, frame

from enum import Enum
import pandas as pd


class _time(Enum):
    select = ["Timestamp", "TimeDelta"]
    renames = {"Timestamp": "TS", "TimeDelta": "V"}


class response:
    time = _time


class _cpuusage(Enum):
    select = ["Timestamp", "CPUPercUsage"]
    renames = {"Timestamp": "TS", "CPUPercUsage": "V"}


class cpu:
    usage = _cpuusage


class _memoryusage(Enum):
    select = ["Timestamp", "MemoryPercUsage"]
    renames = {"Timestamp": "TS", "MemoryPercUsage": "V"}


class memory:
    usage = _memoryusage


class _latency(Enum):
    select = ["Timestamp", "Latency"]
    renames = {"Timestamp": "TS", "Latency": "V"}


class _throughput(Enum):
    select = ["Timestamp", "Throughput"]
    renames = {"Timestamp": "TS", "Throughput": "V"}


class request:
    latency = _latency
    throughput = _throughput


class Set:
    def __init__(self, data: ds.Set) -> None:
        ng = getattr(data.network, "general")
        sc = getattr(data.structure, "container")
        hr = getattr(data.http, "result")
        hm = getattr(data.http, "metrics")

        # TODO get latencies from http.result
        # WARN enable http.result by default in experiments
        if hr.empty:
            hr = hm

        self.response = frame.Frame(time=ng[response.time.select.value])
        self.response.rename(time=response.time.renames.value)

        self.cpu = frame.Frame(usage=sc[cpu.usage.select.value])
        self.cpu.rename(usage=cpu.usage.renames.value)

        self.memory = frame.Frame(usage=sc[memory.usage.select.value])
        self.memory.rename(usage=memory.usage.renames.value)

        self.request = frame.Frame(latency=hr[request.latency.select.value], throughput=hm[request.throughput.select.value])
        self.request.rename(latency=request.latency.renames.value, throughput=request.throughput.renames.value)

        self.stats = self._describe()

    def _describe(self):
        cu = getattr(self.cpu, "usage").describe().rename(dict(V="cpu usage"), axis=1).T
        mu = getattr(self.memory, "usage").describe().rename(dict(V="memory usage"), axis=1).T
        rql = getattr(self.request, "latency").describe().rename(dict(V="request latency"), axis=1).T
        rqt = getattr(self.request, "throughput").describe().rename(dict(V="request throughput"), axis=1).T
        rst = getattr(self.response, "time").describe().rename(dict(V="response time"), axis=1).T
        return pd.concat([cu, mu, rql, rqt, rst])
