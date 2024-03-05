from xa.proc import ds, frame

from enum import Enum
import pandas as pd
import scipy.stats as st
import numpy as np


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

        self.stats = self._stats()

    def _stats(self):
        m = getattr(self.cpu, "usage")
        cu = m.describe().rename(index=dict(std="std unbias"), columns=dict(V="cpu usage")).T
        cu.insert(2, "std bias", m.V.std(ddof=0))
        cu["ci 95% -"], cu["ci 95% +"] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())
        cu["ci 99% -"], cu["ci 99% +"] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())

        m = getattr(self.memory, "usage")
        mu = m.describe().rename(index=dict(std="std unbias"), columns=dict(V="memory usage")).T
        mu.insert(2, "std bias", m.V.std(ddof=0))
        mu["ci 95% -"], mu["ci 95% +"] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())
        mu["ci 99% -"], mu["ci 99% +"] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())

        m = getattr(self.request, "latency")
        rql = m.describe().rename(index=dict(std="std unbias"), columns=dict(V="request latency")).T
        rql.insert(2, "std bias", m.V.std(ddof=0))
        rql["ci 95% -"], rql["ci 95% +"] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())
        rql["ci 99% -"], rql["ci 99% +"] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())

        m = getattr(self.request, "throughput")
        rqt = m.describe().rename(index=dict(std="std unbias"), columns=dict(V="request throughput")).T
        rqt.insert(2, "std bias", m.V.std(ddof=0))
        rqt["ci 95% -"], rqt["ci 95% +"] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())
        rqt["ci 99% -"], rqt["ci 99% +"] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())

        m = getattr(self.response, "time")
        rst = m.describe().rename(index=dict(std="std unbias"), columns=dict(V="response time")).T
        rst.insert(2, "std bias", m.V.std(ddof=0))
        rst["ci 95% -"], rst["ci 95% +"] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())
        rst["ci 99% -"], rst["ci 99% +"] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())

        return pd.concat([cu, mu, rql, rqt, rst])

    def _restats(self):
        self.stats = self._stats()

    def _iqrclean(self, cuT, muT, rqlT, rqtT, rstT):
        self.cpu.iqrclean(usage=dict(V=cuT))
        self.memory.iqrclean(usage=dict(V=muT))
        self.request.iqrclean(latency=dict(V=rqlT))
        self.request.iqrclean(throughput=dict(V=rqtT))
        self.response.iqrclean(time=dict(V=rstT))
