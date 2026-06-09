import pm4py
import pandas as pd

# Read the .xes file
log = pm4py.read_xes('data/BPI_Challenge_2019.xes')

# Convert to DataFrame
df = pm4py.convert_to_dataframe(log)

# Save as CSV
df.to_csv('data/BPI_Challenge_2019.csv', index=False)







