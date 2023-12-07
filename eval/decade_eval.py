import pandas as pd

df = pd.read_csv('../data/eval/year_eval.csv')
df['decade'] = df['year'] // 10 * 10
df = df.drop(columns=['year'])
df = df.groupby('decade').mean().reset_index()
df = df.round(1)
df.to_csv('../data/eval/decade_eval.csv', index=False)