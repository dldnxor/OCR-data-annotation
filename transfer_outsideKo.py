import json
import os

note = {}

os.chdir("/opt/ml/input/data/test/ufo")
file_list = os.listdir()
# print(file_list)

# points tag
for i in file_list:
    with open(i, 'r') as book:        
        data = json.load(book)
        # print(data)
        note[i] = {}
        note[i]["img_h"] = data["images"][0]["height"]
        note[i]["img_w"] = data["images"][0]["width"]
        note[i]['words'] = {}
        for j in data['annotations']:
            # print(j)            
            note[i]['words'][j['id']] = {}
            note[i]['words'][j['id']]['points'] = []
            ## point 추가 ##
            ## x, y, w, h
            ## [x, y] [x+width, y]  [x+width, y+height] [x, y+height]
            

            
            note[i]['words'][j['id']]['transcription'] =  j['text']
            note[i]['words'][j['id']]['language'] = ['ko']
            note[i]['words'][j['id']]['illegibility'] = False
            note[i]['words'][j['id']]['orientation'] = "Horizontal"
            note[i]['words'][j['id']]['word_tags'] = None
            

# tags
        note[i]["tags"] = None
        
# license tags
        license ={
                        "usability": True,
                        "public": True,
                        "commercial": True,
                        "type": "CC-BY-SA",
                        "holder": None
                    }
        note[i]["license_tag"] = license


# note = json.dumps(note)
# print(type(note))
print(note)