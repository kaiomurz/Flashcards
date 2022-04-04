import numpy as np
import pandas as pd
data = pd.DataFrame(columns=['a','b'])
data.to_csv('test_data.csv')
test_data = pd.read_csv('test_data.csv')

print(test_data.head())
a = np.arange(10)
print(a)
print("test")