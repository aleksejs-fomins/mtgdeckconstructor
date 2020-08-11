import os
import pandas as pd


def load_collection(path):
    return pd.read_hdf(path)


def save_collection(path, df):
    df.to_hdf(path, key='collection', mode='w')


def update_collection(path, df):
    if os.path.isfile(path):
        # 1. Load dataframe from h5 collection
        dfOld = load_collection(path)

        # 2. Merge new dataframe into old one
        for idx, row in df.iterrows():
            if row['name'] in dfOld['name']:
                dfOld = dfOld[dfOld['name'] != row['name']]

        dfNew = pd.concat([dfOld, df])
    else:
        dfNew = df

    # 3. Save dataframe back to h5
    save_collection(path, dfNew)


def query_collection(df, queryDict):
    queryDictEff = queryDict.copy()
    if 'type' in queryDictEff:
        queryDictEff['type_line'] = queryDictEff.pop('type')
    return pd_query_partial(df, queryDictEff)


# Get rows for which several columns have some exact values
def pd_query_partial(df, queryDict):
    dfRez = df.copy()
    for k,v in queryDict.items():
        # print(dfRez[k].str.lower())

        dfRez = dfRez[dfRez[k].str.lower().str.contains(v.lower())]

    return dfRez



    # if len(queryDict) == 0:
    #     return df
    # else:
    #     # Query likes strings to be wrapped in quotation marks for later evaluation
    #     strwrap = lambda val: '"' + val + '"' if isinstance(val, str) else str(val)
    #     query = ' and '.join([colname + '==' + strwrap(val) for colname, val in queryDict.items()])
    #     return df.query(query, )
