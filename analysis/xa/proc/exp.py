from xa.io import src
from xa.proc import ds, ms

import pandas as pd


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

    def _stats(self):
        v = [f.metric.stats for f in self.i]
        k = [j for j in self.__dict__ if j not in ["name", "i"]]
        df = pd.concat(v, keys=k)
        df.index.names = ["iter", "stat"]
        return df
