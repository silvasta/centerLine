
#import modules.JsonHandler 
from modules.JsonHandler import *
from modules.JsonDisplayer import *

def load_test():
        #test with class 
    #importedJSON = JsonHandler("Peter")
    #importedJSON.say_hi()
        #test with function import
    importedJSON = importJson("/home/ss/Desktop/Dataset/Test/person_keypoints_test2019.json")
        
    print("import successful")
    #print(importedJSON)



def write_test():
    aList = [{"a":54, "b":87}, {"c":81, "d":63}, {"e":17, "f":39}]
    writeJson(aList, path = "data2.json")
    print("write successful")


def display_test(path):
    importedJSON = importJson(path)
    # importedJSON = importJson("data2.json")
    #importedJSON = importJson("/home/ss/ownCloud/bachelor thesis/data/annotated_lines_on_robocup_dataset/Test/1.json")

    displayJson(importedJSON)
    print("display successful")



def main():

    print("Hello and Welcome to the JSON demonstration")
    
#    load_test()
#    write_test()
#    path = "/home/ss/Desktop/Dataset/Train/person_keypoints_train2019.json"
#    display_test(path)
#    path = "/home/ss/Desktop/Dataset/Test/person_keypoints_test2019.json"
    #path = "/home/ss/ownCloud/bachelor thesis/code/src/tools/json/annotations/captions_train2017.json" 
    #path = "/home/ss/ownCloud/bachelor thesis/code/src/tools/json/annotations/instances_train2017.json" 
    #path = "/home/ss/ownCloud/bachelor thesis/code/src/tools/json/annotations/person_keypoints_val2017.json"
    #path = "/home/ss/ownCloud/bachelor thesis/data/annotated_lines_on_robocup_dataset/Test/47.json"
    path = "/home/ss/ownCloud/bachelor thesis/data/roboline/annotations/roboline_test.json"
   # path = "/home/ss/ownCloud/bachelor thesis/data/random_test.json"

    
    path = "/home/ss/ownCloud/bachelor thesis/data/random_synthetic_image/annotations/random_4lines_val.json"

    path = "/home/ss/Downloads/random_4categories_train.json"
    display_test(path)
    
    #path = "/home/ss/ownCloud/bachelor thesis/data/random_test_after.json"

    #display_test(path)
    
    print("End of the Demonstration")


if __name__ == '__main__':
    main()


