import os
import json
import numpy as np

path1 = "/opt/ml/input/data/upstage/ufo/train.json"
nopoly_json = "/opt/ml/input/data/no_poly.json"

fpath="/opt/ml/input/data/upstage/images/"
file1=json.load(open(path1,'r', encoding='utf-8'))
fname=[i for i in file1['images']]

for k in fname:
    for word_info in file1['images'][k]['words'].values():
        if len(np.array(word_info['points']).flatten()) >8:
            pathh=fpath+k
            if os.path.exists(pathh):
                os.remove(pathh)
            if k in file1['images']:
                file1['images'].pop('{}'.format(k))
            else:
                continue

with open(nopoly_json, 'w') as outfile:
    json.dump(file1, outfile)
