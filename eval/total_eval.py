import numpy as np
from util import createDataFrameFromCSVFolder, createPathIfNotExists


createPathIfNotExists('../data/eval')

def getCAGR(start, end, years):
    return (end/start)**(1/years)-1

def getCAGRFromDataFrame(df):
    start = df['year'].min()
    end = df['year'].max()
    years = end - start + 1
    startValue = df[df['year'] == start]['numberOfMoviesInYear'].values[0]
    endValue = df[df['year'] == end]['numberOfMoviesInYear'].values[0]
    cagr = getCAGR(startValue, endValue, years)
    print(f'Computing CAGR from {start} to {end} with {years} years, start value {startValue} and end value {endValue}: {cagr}')
    return cagr

def getEstimatedCAGRValues(df):
    CAGR = getCAGRFromDataFrame(df)
    startValue = df[df['year'] == df['year'].min()]['numberOfMoviesInYear'].values[0]
    df['estimatedNumberOfMoviesInYear'] = df.apply(lambda row: startValue * (1 + CAGR)**(row['year'] - df['year'].min()), axis=1).round(0)
    return df


df = createDataFrameFromCSVFolder('../data/total')
df = df.sort_values(by=['year'])
df = df.reset_index(drop=True)
df['numberOfMoviesInYear'] = df['numberOfMoviesInYear'].astype(float)
df['decade'] = df['year'] // 10 * 10
for decade in list(df['decade'].unique()):
    decade_str = str(decade) + 's yearly mean'
    decade_mean = np.mean(df[df['decade'] == decade]['numberOfMoviesInYear']).astype(int)
    df[decade_str] = df.apply(lambda row: decade_mean if row['decade'] == decade else np.nan, axis=1)
    
df = df.drop(columns=['decade'])
df = getEstimatedCAGRValues(df)
df.to_csv('../data/eval/total.csv', index=False)