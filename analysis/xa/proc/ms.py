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
        cu["ci 95%"] = [st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())]
        cu["ci 99%"] = [st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())]
        # cu.columns = [[""] * len(cu.columns), cu.columns]
        # cu[[("ci", "95% +"), ("ci", "95% -")]] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.std())
        # cu[[("ci", "99% +"), ("ci", "99% -")]] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.std())

        m = getattr(self.memory, "usage")
        mu = m.describe().rename(index=dict(std="std unbias"), columns=dict(V="memory usage")).T
        mu.insert(2, "std bias", m.V.std(ddof=0))
        mu["ci 95%"] = [st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())]
        mu["ci 99%"] = [st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())]
        # mu.columns = [[""] * len(mu.columns), mu.columns]
        # mu[[("ci", "95% +"), ("ci", "95% -")]] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.std())
        # mu[[("ci", "99% +"), ("ci", "99% -")]] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.std())

        m = getattr(self.request, "latency")
        rql = m.describe().rename(index=dict(std="std unbias"), columns=dict(V="request latency")).T
        rql.insert(2, "std bias", m.V.std(ddof=0))
        rql["ci 95%"] = [st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())]
        rql["ci 99%"] = [st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())]
        # rql.columns = [[""] * len(rql.columns), rql.columns]
        # rql[[("ci", "95% +"), ("ci", "95% -")]] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.std())
        # rql[[("ci", "99% +"), ("ci", "99% -")]] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.std())

        m = getattr(self.request, "throughput")
        rqt = m.describe().rename(index=dict(std="std unbias"), columns=dict(V="request throughput")).T
        rqt.insert(2, "std bias", m.V.std(ddof=0))
        rqt["ci 95%"] = [st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())]
        rqt["ci 99%"] = [st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())]
        # rqt.columns = [[""] * len(rqt.columns), rqt.columns]
        # rqt[[("ci", "95% +"), ("ci", "95% -")]] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.std())
        # rqt[[("ci", "99% +"), ("ci", "99% -")]] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.std())

        m = getattr(self.response, "time")
        rst = m.describe().rename(index=dict(std="std unbias"), columns=dict(V="response time")).T
        rst.insert(2, "std bias", m.V.std(ddof=0))
        rst["ci 95%"] = [st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.sem())]
        rst["ci 99%"] = [st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.sem())]
        # rst.columns = [[""] * len(rst.columns), rst.columns]
        # rst[[("ci", "95% +"), ("ci", "95% -")]] = st.norm.interval(confidence=0.95, loc=m.V.mean(), scale=m.V.std())
        # rst[[("ci", "99% +"), ("ci", "99% -")]] = st.norm.interval(confidence=0.99, loc=m.V.mean(), scale=m.V.std())

        return pd.concat([cu, mu, rql, rqt, rst])
