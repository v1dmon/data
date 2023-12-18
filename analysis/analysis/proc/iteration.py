from analysis.io import logfile
from analysis.proc import dataset


class Iteration:
    def __init__(self, path: str, gzip: bool = True) -> None:
        self.src = logfile.getLogFiles(path, gzip)
        self.data = dataset.DataSet(self.src)
        self.metric = dataset.MetricSet(self.data)
