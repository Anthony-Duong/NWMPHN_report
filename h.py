import pandas as pd

df = pd.DataFrame([['Bad', 'Male', 1542],
                   ['Good', 'Male', 1419],
                   ['Good', 'Female', 714],
                   ['Bad', 'Female', 419],
                   ['Neutral', 'Male', 254],
                   ['Neutral', 'Female', 138], 
                   ['Bad', 'Genderless', 9], 
                   ['Good', 'Genderless', 4],
                   ['Neutral', 'Genderless', 3], 
                   ['Reformed', 'Male', 2]])
df.columns = ['ALIGN', 'SEX', 'n']

outer = df.groupby('SEX').sum()
inner = df.groupby(['SEX', 'ALIGN']).sum()
inner_labels = inner.index.get_level_values(1)

print(outer.values.flatten()[1::2])
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(24,12))
size = 0.3

ax.pie(outer.values.flatten()[1::2], radius=1,
       labels=outer.index,
       autopct='%1.1f%%',
       wedgeprops=dict(width=size, edgecolor='w'))

ax.pie(inner.values.flatten(), radius=1-size, 
       labels = inner_labels,
       wedgeprops=dict(width=size, edgecolor='w'))

ax.set(aspect="equal", title='Pie plot with `ax.pie`')
plt.show()