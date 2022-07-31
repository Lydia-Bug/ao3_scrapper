import pandas as pd  ##Dependency
import plotly.express as px ##Dependency
import numpy as np

data = pd.read_csv('wallworksrate.csv', index_col=0)

x_axis = "dates"
y_axis = "rate"

plot_data = {
  x_axis: data[x_axis],
  y_axis: data[y_axis]
}
#load data into a DataFrame object:
df = pd.DataFrame(plot_data)
fig = px.line(df, x=x_axis, y=y_axis)
fig.show()