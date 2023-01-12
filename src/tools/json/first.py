import json

with open('/home/ss/Desktop/Dataset/Test/person_keypoints_test2019.json') as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

#jsonObject
#print(jsonObject["categories"])

#print(len(jsonObject["images"]))

a_dictionary = jsonObject
dictionary_items = a_dictionary.items()
for item in dictionary_items:
    print(item)
    print()
