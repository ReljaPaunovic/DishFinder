import json

a = json.load(open("tokenized_ingredients_from_allrecipes.json"))
b = json.load(open("tokenized_ingredients_from_BBC.json"))

print a[0]

z = a[0].copy()
z.update(b[0])

with open('tokenized_ingredients_from_BBC_and_allrecipes.json', 'w') as outfile:
    json.dump(z,outfile,indent=4)