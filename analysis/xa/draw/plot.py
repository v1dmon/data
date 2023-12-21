import matplotlib
import matplotlib.pyplot as plt

matplotlib.interactive(False)


class _Plot:
    def add(self, ax, **kwargs):
        pass


class Pairwise(_Plot):
    def __init__(self, x, y, title, label, **kwargs) -> None:
        self.x, self.y = x, y
        self.title = title
        self.label = label
        self.kwargs = kwargs

    def add(self, ax, **kwargs):
        ax.plot(self.x, self.y, label=self.label, **kwargs)
        ax.set_title(self.title)
        ax.set(**self.kwargs)


class Figure:
    def __init__(
        self,
        ncols,
        *args,
        title: str,
        title_props: dict,
        subplots_props: dict,
        legend_props: dict,
    ) -> None:
        self.__row, self.__col = 0, 0
        self.__ncols = ncols
        self.__cc = plt.rcParams["axes.prop_cycle"]()

        nargs = len(args)
        self.__nrows = ((nargs // ncols) + (nargs % ncols)) or 1

        self.fig, self.__ax = plt.subplots(nrows=self.__nrows, ncols=self.__ncols, **subplots_props)
        self.fig.suptitle(title, **title_props)

        self.__add(*args)
        self.__delaxes()

        self.fig.legend(**legend_props)

        plt.close(self.fig)

    def __add(self, *args: _Plot):
        for plot in args:
            if self.__ncols == 1:
                ax = self.__ax[self.__row]
            elif self.__nrows == 1:
                ax = self.__ax[self.__col]
            else:
                ax = self.__ax[self.__row, self.__col]
            plot.add(ax, color=next(self.__cc)["color"])
            self.__next()

    def __next(self):
        self.__col += 1
        if self.__col >= self.__ncols:
            self.__col = 0
            self.__row += 1

    def __delaxes(self):
        for ax in self.__ax.flat:
            if not ax.has_data():
                self.fig.delaxes(ax)


# import plotly.subplots as sp


# class Trace:
#     def __init__(self, graph_object, name, xaxis_props, yaxis_props, **kwargs) -> None:
#         self.row, self.col = 0, 0
#         self.name = name
#         self.xaxis_props, self.yaxis_props = xaxis_props, yaxis_props
#         self.go = graph_object(**kwargs)


# class Figure2:
#     def __init__(self, cols, subplots_props, layout_props, **kwargs) -> None:
#         self.row, self.col = 1, 1
#         self.cols = cols
#         self._set(**kwargs)

#         self.rows = ((self.nto // self.cols) + (self.nto % self.cols)) or 1
#         subplots_props["subplot_titles"] = [to.name for to in kwargs.values()]
#         self.figure = sp.make_subplots(self.rows, self.cols, **subplots_props)

#         self._add()

#         self._layout(**layout_props)

#     def _set(self, **kwargs):
#         self.nto = len(kwargs)
#         self.to = []
#         for k, to in kwargs.items():
#             if not isinstance(to, Trace):
#                 raise TypeError(f"{to.__class__} is not T")
#             setattr(self, k, to)
#             self.to.append(getattr(self, k))

#     def _add(self):
#         for to in self.to:
#             to.row, to.col = self.row, self.col
#             self.figure.add_trace(to.go, self.row, self.col)
#             self._next()

#     def _next(self):
#         self.col += 1
#         if self.col > self.cols:
#             self.col = 1
#             self.row += 1

#     def _layout(self, **kwargs):
#         for to in self.to:
#             self.figure.update_xaxes(to.xaxis_props, row=to.row, col=to.col)
#             self.figure.update_yaxes(to.yaxis_props, row=to.row, col=to.col)
#         self.figure.update_layout(**kwargs)

#     def show(self):
#         self.figure.show()
