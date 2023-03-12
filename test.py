import umap
import pandas as pd
import numpy as np
data=pd.read_csv('/home/maria/NYCCrimesAndTaxis/data/borough_hist_merged.csv')

# Drop the Date and DayOfWeek columns
merged_df = data.drop(columns=['Date', 'DayOfWeekNum'])

# Convert the DataFrame to a NumPy array
data = merged_df.to_numpy(dtype=np.float32)

mapper = umap.UMAP().fit(data)

import umap.plot

umap.plot.points(mapper)