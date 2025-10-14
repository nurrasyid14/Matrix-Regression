#scatter_plot.py

import plotly.express as px
from .base_plotter import BasePlotter

class ScatterPlot(BasePlotter):
    """
    Interactive scatter plot for feature relationships.
    """

    def plot(self, df, x_col, y_col, color=None, size=None):
        fig = px.scatter(
            df, x=x_col, y=y_col,
            color=color, size=size,
            title=self.title or f"{x_col} vs {y_col}",
            template="plotly_white"
        )
        self._finalize(fig)
