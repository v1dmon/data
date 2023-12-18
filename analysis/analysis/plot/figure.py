import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Grid:
    def __init__(self, rows, cols, **kwargs) -> None:
        self.rows, self.cols = rows, cols
        self.row, self.col = 1, 1
        self.figure = make_subplots(rows=rows, cols=cols, **kwargs)

    # def addToRow(self, trace):
    #     self.col = 1
    #     self.row += 1
    #     self.figure.append_trace(trace, self.row, self.col)
    #     self.col += 1

    # def addToCol(self, trace):
    #     self.figure.append_trace(trace, self.row, self.col)
    #     self.col += 1

    def add(self, trace):
        self.figure.append_trace(trace, self.row, self.col)
        self.col += 1
        if self.col > self.cols:
            self.col = 1
            self.row += 1

    def layout(self, **props):
        self.figure.update_layout(**props)

    def show(self):
        self.figure.show()

    def write(self):
        pass
