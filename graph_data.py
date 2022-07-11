##import seaborn as sns  ##Dependency
import pandas as pd  ##Dependency
##import matplotlib.pyplot as plt ##Dependency
##from bokeh.plotting import figure, output_file, show ##Dependency
##from bokeh.palettes import magma ##Dependency
import plotly.express as px ##Dependency

data = pd.read_csv('scrapper.csv', index_col=0)
print(data.head(10))

# instantiating the figure object
# reading the database

  
# plotting the scatter char
fig = px.scatter(data, x="words", y="kudos")
  
# showing the plot
fig.show()