import json

path1 = "/opt/ml/input/data/annotations/images/annotation.json"
path2 = "/opt/ml/input/data/ICDAR17_All/ufo/train.json"

merged_json = "/opt/ml/input/data/merged.json"

file_list = []

file1 = json.load(open(path1, 'r'))
file_list.append(file1)

file2 = json.load(open(path2, 'r'))
file_list.append(file2)

new_json = {}

for file in file_list:
    image = file['images']
    
    for jpg in image:
        new_json[jpg] = image[jpg]

merged = {'images' : new_json}
        
with open(merged_json, 'w') as outfile:
    json.dump(merged, outfile)



    

