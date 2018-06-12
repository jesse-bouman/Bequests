import plotly.graph_objs as go
import plotly.offline
import colorlover as cl
from plotly import tools
from plotly.offline import init_notebook_mode
import plotly.dashboard_objs as dashboard

#init_notebook_mode(connected=True)

import numpy as np

print(cl.scales['11']['qual']['Paired'])
def plot(x, y, title=""):
    data = go.Scatter(x=x, y=y)
    plotly.offline.plot([data])


def plot_stats(e_list, w_list, c_list, lorentz):
    x, y = lorentz
    layout = go.Layout(yaxis=dict(
        range=[0, 1]), xaxis=dict(range=[0,1]))
    fig = tools.make_subplots(rows=2, cols=2)
    fig.append_trace(go.Histogram(x=e_list), 1, 1)
    fig.append_trace(go.Histogram(x=w_list), 1, 2)
    fig.append_trace(go.Histogram(x=c_list), 2, 1)
    fig.append_trace( go.Scatter(x=w_list, y=np.array(c_list)/np.array(w_list)), 2, 2)
    fig['layout']['yaxis4'].update(range=[0,1])
    plotly.offline.plot(fig)

x = [0, 1, 2]
y = [0, 1, 4]

