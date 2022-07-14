##import seaborn as sns  ##Dependency
import pandas as pd  ##Dependency
##import matplotlib.pyplot as plt ##Dependency
##from bokeh.plotting import figure, output_file, show ##Dependency
##from bokeh.palettes import magma ##Dependency
import plotly.express as px ##Dependency
import numpy as np

data = pd.read_csv('test2.csv', index_col=0)

x_axis = "words"
y_axis = "kudos"

x_axis_data = data[x_axis]
y_axis_data = data[y_axis]

# plotting the scatter char
fig = px.scatter(x=x_axis_data, y=y_axis_data, labels={
                     "x": x_axis,
                     "y": y_axis
                 })
  
x_axis_percent = 0.99
y_axis_percent = 0.99

x_axis_length = np.quantile(x_axis_data, x_axis_percent)
y_axis_length = np.quantile(y_axis_data, y_axis_percent)

fig.update_layout(xaxis_range=[-0.05*x_axis_length,x_axis_length+0.05*x_axis_length])
fig.update_layout(yaxis_range=[-0.05*y_axis_length,y_axis_length+0.05*x_axis_length])

fig.show()
