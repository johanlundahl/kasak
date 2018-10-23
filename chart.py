class StackedBar():
    def __init__(self, title, labels):
        self._data = []
        self._title = title
        self._labels = labels
    
    @property
    def title(self):
        return self._title
    
    @property
    def labels(self):
        return self._labels
    
    def add_bar(self, name, serie, color):
        self._data.append((name, serie, color))
    
    def get_bars(self):
        return self._data
        