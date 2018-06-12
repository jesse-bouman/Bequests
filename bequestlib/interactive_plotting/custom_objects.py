import colorlover as cl
from plotly import graph_objs as go

COLORMAP = cl.scales['11']['qual']['Paired']


class Graph:
    def __init__(self, df, plotly_graph, measure, x_axis, colors=None, filters=None, slider=None):
        self.df = df
        self.measure = measure
        self.x = x_axis
        self.colors = colors
        self.filters = self.catch_empty(filters)
        self.slider = self.catch_empty(slider)
        self.gr = plotly_graph
        self.traces = self.prepare_data()

    @staticmethod
    def make_list(m):
        if not type(m) == list:
            return [m]
        else:
            return m

    @staticmethod
    def catch_empty(m):
        if m is None:
            return []
        else:
            return Graph.make_list(m)

    @property
    def needed_cols(self):
        return [self.measure] + [self.x] + self.filters + self.slider + self.catch_empty(self.colors)

    @property
    def group_by_cols(self):
        return self.filters + self.slider + self.catch_empty(self.colors) + [self.x]

    def aggregate(self):
        return self.df[self.needed_cols].groupby(self.group_by_cols, as_index=False).sum()

    def prepare_data(self):
        data = self.aggregate()
        out_list = list()
        if self.colors:
            un_c = self.df[self.colors].unique()
            for i, col in enumerate(un_c):
                subdata = data[data[self.colors] == col]

                data_i = self.gr(
                    y=subdata[self.measure],
                    x=subdata[self.x],
                    name=col,
                    legendgroup=col,
                    showlegend=False,
                    marker=dict(
                        color=COLORMAP[(2 * i + 1) % 11])
                )
                out_list.append(data_i)
        return out_list

    def showlegend(self):
        for trace in self.traces:
            trace['showlegend'] = True

    def hidelegend(self):
        for trace in self.traces:
            trace['showlegend'] = False

    @staticmethod
    def number_format(number):
        if 1000 <= number < 1e6:
            num = '{:.7g}'.format(number/1000)
            return f'{num} k'
        elif 1e6 <= number < 1e9:
            num = '{:.7g}'.format(number / 1e6)
            return f'{num} M'
        elif number >= 1e9:
            num = '{:.7g}'.format(number / 1e9)
            return f'{num} B'
        else:
            return str(number)

    def add_hover_totals(self):
        data = self.aggregate()
        total = data[[self.measure, self.x]].groupby(self.x).sum()[self.measure].values
        text = ['Total: ' + self.number_format(total_i) for total_i in total]
        self.traces[0]['text'] = text


class Bar(Graph):
    def __init__(self, df, measure, x_axis, colors=None, filters=None, slider=None):
        super().__init__(df, go.Bar, measure, x_axis, colors, filters, slider)
        self.add_hover_totals()


class Scatter(Graph):
    def __init__(self, df, measure, x_axis, colors=None, filters=None, slider=None):
        super().__init__(df, go.Scatter, measure, x_axis, colors, filters, slider)


class LineDivision(Graph):
    def __init__(self, df, numerator, denominator, x_axis, colors=None):
        self.num = numerator
        self.den = denominator
        super().__init__(df, go.Scatter, 'tmp', x_axis, colors, None, None)

    @property
    def needed_cols(self):
        return [self.num] + [self.den] + [self.x] + [self.colors]

    def aggregate(self):
        data = super().aggregate()
        data['tmp'] = data[self.num]/data[self.den]
        return data
