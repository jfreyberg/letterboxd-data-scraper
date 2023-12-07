import pandas as pd
from util import createDataFrameFromCSVFolder, createPathIfNotExists

TOP = 250

def computePercentages(df, columns, totalColumn):
    for column in columns:
        df[column] = df[column] / df[totalColumn] * 100
        df[column] = df[column].round(1)
    return df

df = createDataFrameFromCSVFolder('../data/years')
df = df[df['number'] <= TOP]
df = df.drop(columns=['number', 'slug'])


df['Fifth or More'] = df['partOfFranchise'] > 4
df['Fourth'] = df['partOfFranchise'] == 4
df['Third'] = df['partOfFranchise'] == 3
df['Second'] = df['partOfFranchise'] == 2
df['First'] = df.apply(lambda row: row['partOfFranchise'] == 1 and row['inFranchise'] == True and row['franchiseLength'] > 1, axis=1)
df['Solo'] = df.apply(lambda row: row['partOfFranchise'] == 1 and row['inFranchise'] == False, axis=1)

df['totalMovies'] = 1
df = df.groupby('year').sum().reset_index()
df = df.rename(columns={'inFranchise': 'franchiseMovies'})

total_first_parts = df['First'].sum()
total_second_parts = df['Second'].sum()
missing_second_parts = total_first_parts-total_second_parts
print(total_first_parts)
print(total_second_parts)
print(missing_second_parts/total_first_parts*100)


df = computePercentages(df, ['First', 'Second', 'Third', 'Fourth', 'Fifth or More', 'Solo'], 'totalMovies')
df.to_csv('../data/eval/year_eval.csv', index=False)