# import pandas
import pandas as pd
import numpy as np
from util import createDataFrameFromCSVFolder
from sklearn.linear_model import LinearRegression

# read the csv file
df = createDataFrameFromCSVFolder('../data/collections')

# order by franchise, movie_nr
df = df.sort_values(['franchise', 'part'])
df['franchise'] = df['franchise'].str.replace(' Collection', '')
df = df[(df['franchiseLength'] > 2) & (df['franchiseLength'] < 11)]

# for each movie, append a column with the average score of the franchise
df['rating_avg'] = df.groupby(['franchise'])['rating'].transform('mean')
 
df['rating_diff_avg'] = np.round(df['rating'] - df['rating_avg'], 2)
 
# calculate relative difference
df['rating_rel_avg'] = np.round(df['rating_diff_avg'] / df['rating_avg'] * 100, 0)
 
# round the rating to 2 decimals
df['rating_avg'] = np.round(df['rating_avg'], 2)
 
# rating better, equal or worse than previous/first movie?
df['quality_avg'] = df['rating_diff_avg'].apply(lambda x: 'better' if x > 0 else ('equal' if x == 0 else 'worse')) 
 
# save the dataframe to a new csv file
df = df[['franchise', 'part', 'title', 'year', 'franchiseLength', 'rating', 'rating_avg', 'rating_diff_avg', 'rating_rel_avg', 'quality_avg']]
df.to_csv('../data/eval/collections.csv', index=False)
print(df)

# compute linear relationship between part and rating_rel_avg
X = df[['part']]
y = df['rating_rel_avg']
reg = LinearRegression().fit(X, y)
print(reg.coef_)

# compute average rating per number of movies in franchise
print(df[['franchiseLength', 'rating']].groupby(['franchiseLength']).mean().reset_index())

# compute average rating per number of movies in franchise
df_tmp = df[['part', 'rating']].groupby(['part']).mean().reset_index()
df_tmp['rating_rel'] = (df_tmp['rating'] / df_tmp['rating'].mean() - 1) * 100
print(df_tmp)

df['last'] = df['part'] == df['franchiseLength']
print(df[['last', 'rating']].groupby(['last']).mean().reset_index())

# parts per year
df_tmp = df[['year', 'part', 'rating']].groupby(['year', 'part']).count().reset_index().rename(columns={'rating': 'count'})
# move part to columns
df_tmp = df_tmp.pivot(index='year', columns='part', values='count').reset_index()
df_tmp.to_csv('../data/eval/parts_per_year.csv', index=False)

