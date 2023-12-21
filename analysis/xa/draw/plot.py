import plotly.subplots as sp


class Trace:
    def __init__(self, graph_object, name, xaxis_props, yaxis_props, **kwargs) -> None:
        self.row, self.col = 0, 0
        self.name = name
        self.xaxis_props, self.yaxis_props = xaxis_props, yaxis_props
        self.go = graph_object(**kwargs)


class Figure:
    def __init__(self, cols, subplots_props, layout_props, **kwargs) -> None:
        self.row, self.col = 1, 1
        self.cols = cols
        self._set(**kwargs)

        self.rows = ((self.nto // self.cols) + (self.nto % self.cols)) or 1
        subplots_props["subplot_titles"] = [to.name for to in kwargs.values()]
        self.figure = sp.make_subplots(self.rows, self.cols, **subplots_props)

        self._add()

        self._layout(**layout_props)

    def _set(self, **kwargs):
        self.nto = len(kwargs)
        self.to = []
        for k, to in kwargs.items():
            if not isinstance(to, Trace):
                raise TypeError(f"{to.__class__} is not T")
            setattr(self, k, to)
            self.to.append(getattr(self, k))

    def _add(self):
        for to in self.to:
            to.row, to.col = self.row, self.col
            self.figure.add_trace(to.go, self.row, self.col)
            self._next()

    def _next(self):
        self.col += 1
        if self.col > self.cols:
            self.col = 1
            self.row += 1

    def _layout(self, **kwargs):
        for to in self.to:
            self.figure.update_xaxes(to.xaxis_props, row=to.row, col=to.col)
            self.figure.update_yaxes(to.yaxis_props, row=to.row, col=to.col)
        self.figure.update_layout(**kwargs)

    def show(self):
        self.figure.show()
