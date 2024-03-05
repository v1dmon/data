from xa.io import src
from xa.proc import ds, ms

import pandas as pd
import numpy as np
import scipy.stats as st


class Iteration:
    def __init__(self, path: str) -> None:
        self.src = src.find_logs(path)
        self.data = ds.Set(self.src)
        self.metric = ms.Set(self.data)


class Experiment:
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name

        self.i: list[Iteration] = []
        for key, path in kwargs.items():
            setattr(self, key, Iteration(path))
            self.i.append(getattr(self, key))

        self.stats = self._stats()
        self.summary = self._summary()

    def _stats(self):
        v = [f.metric.stats for f in self.i]
        k = [j for j in self.__dict__ if j not in ["name", "i", "stats", "summary"]]
        df = pd.concat(v, keys=k)
        df.index.names = ["iter", "stat"]
        return df

    def _summary(self):
        idx = pd.IndexSlice
        df = pd.DataFrame()

        keys = set(self.stats.index.get_level_values(1))
        for k in keys:
            means = list(self.stats.loc[idx[:, k], idx["mean"]])
            df.loc[k, "mean of means"] = np.mean(means)
            df.loc[k, "std of means bias"] = np.std(means)
            df.loc[k, "std of means unbias"] = np.std(means, ddof=1)

        return df

    def _restats(self):
        for f in self.i:
            f.metric._restats()

        self.stats = self._stats()
        self.summary = self._summary()

    def iqrclean(self, cuT, muT, rqlT, rqtT, rstT):
        for f in self.i:
            f.metric._iqrclean(cuT, muT, rqlT, rqtT, rstT)

        self._restats()
