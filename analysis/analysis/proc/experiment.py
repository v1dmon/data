from analysis.proc import iteration


class Experiment:
    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        for key, path in kwargs.items():
            setattr(self, key, iteration.Iteration(path))
