#histogram.py

import plotly.express as px
from .base_plotter import BasePlotter

class HistogramPlot(BasePlotter):
    """
    Interactive histogram for distribution visualization.
    """

    def plot(self, df, column, color=None, nbins=20):
        fig = px.histogram(
            df, x=column, color=color, nbins=nbins,
            title=self.title or f"Distribution of {column}",
            template="plotly_white"
        )
        self._finalize(fig)
