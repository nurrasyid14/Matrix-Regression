#correlation_heatmap.py

import plotly.express as px
import pandas as pd
from .base_plotter import BasePlotter

class CorrelationHeatmap(BasePlotter):
    """
    Interactive correlation heatmap for numeric columns.
    """

    def plot(self, df):
        corr = df.corr(numeric_only=True)
        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu_r",
            title=self.title or "Correlation Heatmap",
        )
        self._finalize(fig)
