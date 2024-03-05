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

    def iqrclean(self, **kwargs):
        for key1, map in kwargs.items():
            for key2, threshold in map.items():
                df = getattr(self, key1)
                v = getattr(df, key2)
                q1 = v.quantile(0.25)
                q3 = v.quantile(0.75)
                iqr = q3 - q1
                outliers = df[(v < (q1 - threshold * iqr)) | (v > (q3 + threshold * iqr))]
                setattr(self, key1, df.drop(outliers.index))
