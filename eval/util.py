import os
import pandas as pd

def createDataFrameFromCSVFolder(folder, limit=None):
    files = [x.replace('.csv', '') for x in os.listdir(folder)]
    if limit:
        files = sorted([int(x) for x in files])[:limit]
    df = pd.DataFrame()
    c=0
    for file in files:
        if limit != None and c >= limit:
            break
        newDf = pd.read_csv(folder + '/' + str(file) + '.csv')
        if df.empty:
            df = newDf
        else:
            df = pd.concat([df, newDf])
        c+=1
    return df


def createPathIfNotExists(path):
    if not os.path.exists(path):
        os.makedirs(path)
