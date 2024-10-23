import json
maps = json.load(open("scanned_models.json"))
all_models = []
for map in maps:
    all_models.extend(map["models"])

unique_models = list(set(all_models))

print("There are " + str(len(unique_models)) + " unique models.")

model_materials = []

for model in unique_models:
    model_materials.append({"model": model, "materials": "", "prob": 0.0})

json.dump(model_materials, open("model_materials.json", "w"))