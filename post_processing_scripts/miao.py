import json
import re

models = json.load(open("updated_model_materials.json"))

num_of_words = 3


for model in models:
    modelname = model["model"]
    path = ""
    
    words = modelname.split("/")
    if(len(words) == 1): words = words[0]
    else:
        path = words[:-1]
        words = words[-1]

    words = re.sub(r'\d+', '', words)
    words = words.split("_")[:num_of_words]
    words = "_".join(words)
    #words = re.split(r'\d', words)[0]

    
    num_of_similar_models = 0
    flag = True
    if(words != ""):
        for new_model in models:
            if new_model["model"] != modelname:
                new_modelname = new_model["model"]
                
                temp = new_modelname.split("/")
                if(len(temp) == 1): temp = temp[0]
                else: temp = temp[-1]

                if(temp.startswith(words)):
                    print("Old model: " + modelname)
                    print("New model: " + new_modelname)
                    
                    answer = "miao"
                    while answer != "y" and answer != "n":
                        print("Is this a similar model? (y/n) \nAnswer: ")
                        answer = input()
                        if answer == "y":
                            models.remove(new_model)
                            num_of_similar_models += 1
                        elif answer == "n":
                            flag = False
                            #break
                        
                        if answer != "y" and answer != "n":
                            print("Invalid input. Please enter 'y' or 'n'.")
    else:
        print("Strange model: " + modelname)

    
    if(num_of_similar_models > 1 and not flag):
        new_model = model["model"].split("_")[:num_of_words]
        model["model"] = "_".join(new_model)


json.dump(models, open("updated_model_materials2.json", "w"))