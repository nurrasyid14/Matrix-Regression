#pair_plot.py

import plotly.express as px
from .base_plotter import BasePlotter

class PairPlot(BasePlotter):
    """
    Interactive pair plot showing relationships among all numeric columns.
    """

    def plot(self, df, color=None):
        fig = px.scatter_matrix(
            df,
            dimensions=df.select_dtypes(include=['float', 'int']).columns,
            color=color,
            title=self.title or "Pair Plot Matrix",
        )
        self._finalize(fig)
