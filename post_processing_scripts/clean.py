import json
import re
#import pandas as pd

models = json.load(open("updated_model_materials.json"))
simple_materials = [
    ("glass","glass"), 
    ("wood", "wood"),
    ("concrete", "concrete"), 
    ("clay", "clay"), 
    ("metal", "metal"), 
    ("paper", "paper"),
    ("carton", "paper"),
    ("cardboard", "paper"),
    ("plastic", "plastic"),
    ("leaf", "vegetation"),
    ("grass", "vegetation"),
    ("brick", "brick"),
    ("advisor", "flesh")
]

changed = 0
prev_len = len(models)

# Remove models with "maps/" in the model name and changes models 
# names containing the material name
for model in models:
    if("maps/" in model["model"]):
        models.remove(model)
    else:
        for name, material in simple_materials:
            if name in model["model"]:
                model["model"] = name
                model["material"] = material
                model["prob"] = 100
                changed += 1

for model in models:
    if("maps/" in model["model"]):
        models.remove(model)

complex_materials = [
    ("(car|van).+door", "metal"),
    ("(car|van).+grille", "plastic"),
    ("(car|van).+bumper", "plastic"),
    ("(car|van).+headlight", "plastic"),
    ("(car|van).+trunk", "metal"),
    ("(car|van).+tire", "rubber"),
    ("(car|van).+tailgate", "metal"),
    ("(car|van).+hood", "metal"),
    ("_board_", "wood"),
]

# Changes models names containing a regex material name
for model in models:
    for name, material in complex_materials:
        if re.search(name, model["model"]):
            model["model"] = name
            model["material"] = material
            model["prob"] = 100
            changed += 1

# Removes duplicates
models = [dict(t) for t in {frozenset(d.items()) for d in models}]

# Sorts the models by the model name without address(alphabetically)
models = sorted(models, key=lambda x: x["model"].split("/")[-1])

# Sorts the keys in the dictionary
keys_order = ["model", "material", "prob"]
models = [
    {key: d[key] for key in keys_order if key in d}
    for d in models
]



print("Removed " + str(prev_len - len(models)) + " models.")
print("Changed " + str(changed) + " models.")
print("New number of models: " + str(len(models)))

json.dump(models, open("updated_model_materials_b.json", "w"), indent=4)