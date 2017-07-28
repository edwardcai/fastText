# Press COMMAND + ENTER to run a single line in the console
print('Welcome to Rodeo!')

# Press CTRL + ENTER with text selected to run multiple lines
# For example, select the following lines
x = 7
x**2
# and remember to press CTRL + ENTER

# Here is an example of using Rodeo:
# Import packages

import numpy as np
import pandas as pd
import codecs
from matplotlib.colors import LogNorm


_file = '~/Projects/chatbot-data/DCM-258.es.tsv'
df = pd.read_table(_file, delimiter='\t', header=0)
df.head()
low = .05
high = .95
print df.size
for col in ['COSINE_DISTANCE', 'LEV_DISTANCE']:
    high = df[col].quantile(0.95)
    low = df[col].quantile(0.05)
    print high
    print low
    df = df[df[col] < high]
    print df.size
    df = df[df[col] > low]
    print df.size
    
from matplotlib import pyplot as plt
x=df.COSINE_DISTANCE
y=df.LEV_DISTANCE

with plt.style.context('fivethirtyeight'):
    
    plt.hist2d(x, y, bins=15, norm=LogNorm())
    plt.ylabel('LEV')
    plt.xlabel('COSINE')
plt.colorbar()
plt.show()
    


