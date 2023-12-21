from xa.io import src
from xa.proc import ds, ms


class Iteration:
    def __init__(self, path: str) -> None:
        self.src = src.find_logs(path)
        self.data = ds.Set(self.src)
        self.metric = ms.Set(self.data)


class Experiment:
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        for key, path in kwargs.items():
            setattr(self, key, Iteration(path))
