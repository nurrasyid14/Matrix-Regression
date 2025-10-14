#utils.py

import plotly.io as pio

def set_visual_style(theme="plotly_white"):
    """
    Set global Plotly theme.
    """
    pio.templates.default = theme
