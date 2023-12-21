import glob, gzip, json


class Log:
    def __init__(self, path: str) -> None:
        self.path = path
        self.content = []
        with gzip.open(self.path, "rb") as zf:
            for line in zf:
                payload = json.loads(line.decode("utf-8").strip())
                self.content.append(payload)


def find_logs(path: str) -> list[Log]:
    pn = f"{path}/*.log.gz"
    lf: list[Log] = []
    for file in glob.glob(pn):
        lf.append(Log(file))
    return lf
