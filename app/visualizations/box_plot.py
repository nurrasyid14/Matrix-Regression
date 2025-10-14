#box_plot.py

import plotly.express as px
from .base_plotter import BasePlotter

class BoxPlot(BasePlotter):
    """
    Interactive box plot for value distribution and outliers.
    """

    def plot(self, df, column, color=None):
        fig = px.box(
            df, y=column, color=color,
            title=self.title or f"Box Plot of {column}",
            template="plotly_white"
        )
        self._finalize(fig)
