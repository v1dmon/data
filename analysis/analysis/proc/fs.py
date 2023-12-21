import glob
import gzip
import json


class LogFile:
    def __init__(self, path: str, type: bool = True) -> None:
        self.path = path
        self.type = type
        self.content = []
        if self.type:
            with gzip.open(self.path, "rb") as zf:
                for line in zf:
                    payload = json.loads(line.decode("utf-8").strip())
                    self.content.append(payload)


def getLogFiles(path: str, gzip: bool = True) -> list[LogFile]:
    extpath = f"{path}/*.log.gz" if gzip else f"{path}/*.log"
    logfiles: list[LogFile] = []
    for file in glob.glob(extpath):
        logfiles.append(LogFile(file, gzip))
    return logfiles
