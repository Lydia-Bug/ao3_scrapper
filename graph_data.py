import pandas as pd  ##Dependency
import matplotlib.pyplot as plt ##Dependency

data = pd.read_csv('scrapper.csv', index_col=0)
print(data.head(10))

# Scatter plot with day against tip
plt.scatter(data['words'], data['kudos'])
  
# Adding Title to the Plot
plt.title("Scatter Plot")
  
# Setting the X and Y labels
plt.xlabel('words')
plt.ylabel('kudos')
  
plt.show()