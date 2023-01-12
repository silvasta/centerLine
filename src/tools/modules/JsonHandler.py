import json

def importJson(pathToFile):
    with open(pathToFile) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    return jsonObject

def writeJson(dict_to_write, path="data.json"):
    jsonString = json.dumps(dict_to_write)
    jsonFile = open(path, "w")
    jsonFile.write(jsonString)
    jsonFile.close()


