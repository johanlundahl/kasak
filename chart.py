import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio


class StackedBar():
    def __init__(self, x):
        self._data = []
        self._x = x
        self._layout = go.Layout(barmode = 'stack')
        
    def add_bar(self, lst, label = None):
        bar = go.Bar(x = self._x, y = lst, name = label)
        self._data.append(bar)
    
    def save(self, path):
        fig = go.Figure(data = self._data, layout = self._layout)
        pio.write_image(fig, path)