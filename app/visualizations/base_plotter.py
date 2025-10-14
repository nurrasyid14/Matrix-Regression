#base_plotter.py

import plotly.io as pio
from abc import ABC, abstractmethod

class BasePlotter(ABC):
    """
    Abstract base class for all Plotly visualizers.
    """

    def __init__(self, title=None, width=700, height=500, save_path=None):
        self.title = title
        self.width = width
        self.height = height
        self.save_path = save_path

    @abstractmethod
    def plot(self, *args, **kwargs):
        pass

    def _finalize(self, fig):
        fig.update_layout(
            title=self.title,
            width=self.width,
            height=self.height,
            template="plotly_white"
        )

        if self.save_path:
            if self.save_path.endswith(".html"):
                fig.write_html(self.save_path)
            else:
                fig.write_image(self.save_path)

        fig.show()