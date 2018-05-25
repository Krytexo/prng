#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import plotly.offline as pl
import plotly.graph_objs as go

# Create random data with numpy
import numpy as np

N = 1000
random_x = np.random.randn(N)
random_y = np.random.randn(N)

# Create a trace
trace = go.Scatter(
    x = random_x,
    y = random_y,
    mode = 'markers'
)

data = [trace]

# Plot and embed in ipython notebook!
pl.plot(data, filename='basic-scatter', image='png', auto_open=False)

# or plot with: plot_url = py.plot(data, filename='basic-line')
