import plotly.subplots as sp


class Trace:
    def __init__(self, o, **kw) -> None:
        self.t = o(**kw)

    def add(self, fig, r, c):
        self.r, self.c = r, c
        fig.add_trace(self.t, self.r, self.c)
        # TODO set props


class Figure:
    def __init__(self, cx, *to, **kw) -> None:
        self.r, self.c = 1, 1
        self.cx = cx

        self.to = to
        self.n = len(self.to)

        self.rx = ((self.n // self.cx) + (self.n % self.cx)) or 1

        self.f = sp.make_subplots(self.rx, self.cx, **kw)

        for o in self.to:
            self._add(o)

        # TODO update layout

    def _add(self, to):
        to.add(self.f, self.r, self.c)
        self._next()

    def _next(self):
        self.c += 1
        if self.c > self.cx:
            self.c = 1
            self.r += 1

    def show(self):
        self.f.show()
