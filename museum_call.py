import requests
import pandas as pd
import json


my_req = requests.get(url="https://collectionapi.metmuseum.org/public/collection/v1/objects")
var = my_req.json()


ourdata = []


for i in var['objectIDs'][:100]:
    detail = requests.get(url="https://collectionapi.metmuseum.org/public/collection/v1/objects/{}".format(i))
    myjson = detail.json()
    ourdata.append(myjson)


df = pd.DataFrame(ourdata)


loc_to = df.loc[:, ['additionalImages', 'constituents', 'measurements', 'tags']]
for i in loc_to.columns:
    loc_to = loc_to.explode(i)


final_dict = pd.json_normalize(json.loads(loc_to.to_json(orient="records")))


df1 = pd.concat([df, final_dict], axis=1)

df1 = df1.drop(['additionalImages', 'constituents', 'measurements', 'tags'], axis=1)

df1.to_csv('museum_csv.csv', index=False)