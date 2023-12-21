import pandas as pd


class Frame:
    def __init__(self, **kwargs) -> None:
        for key, data in kwargs.items():
            setattr(self, key, pd.DataFrame(data))

    def dtypes(self, **kwargs):
        for key, map in kwargs.items():
            setattr(self, key, getattr(self, key).astype(map))

    def sortBy(self, **kwargs):
        for key, col in kwargs.items():
            setattr(self, key, getattr(self, key).sort_values(col))

    def normalize(self, **kwargs):
        for key, col in kwargs.items():
            setattr(self, key, getattr(self, key).merge(pd.json_normalize(getattr(self, key)[col]), left_index=True, right_index=True))

    def drop(self, **kwargs):
        for key, cols in kwargs.items():
            setattr(self, key, getattr(self, key).drop(columns=cols, errors="ignore"))

    def rename(self, **kwargs):
        for key, map in kwargs.items():
            setattr(self, key, getattr(self, key).rename(columns=map))
