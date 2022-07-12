##import seaborn as sns  ##Dependency
import pandas as pd  ##Dependency
##import matplotlib.pyplot as plt ##Dependency
##from bokeh.plotting import figure, output_file, show ##Dependency
##from bokeh.palettes import magma ##Dependency
import plotly.express as px ##Dependency

data = pd.read_csv('test.csv', index_col=0)
print(data.head(10))

# instantiating the figure object
# reading the database

words = data["words"]
kudos = data["kudos"]

## The x-axis has to be sorted
words = [x for _,x in sorted(zip(words,kudos))]
kudos = sorted(kudos)


# plotting the scatter char
fig = px.scatter(x=words, y=kudos)
  
# showing the plot
fig.show()