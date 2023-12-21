from analysis.proc import fs
from analysis.proc import ds
import pandas as pd


class Iteration:
    def __init__(self, path: str, gzip: bool = True) -> None:
        self.logfiles = fs.getLogFiles(path, gzip)
        self.dataset = ds.DataSet(self.logfiles)


class Experiment:
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        for key, path in kwargs.items():
            setattr(self, key, Iteration(path))
