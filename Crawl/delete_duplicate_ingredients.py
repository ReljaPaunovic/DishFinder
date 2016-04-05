import json
import itertools

data = json.load(open("nouns_ingredients_in_each_recipes.json"))
b = []

for i in data:
	new = set(i) - set(b)
	b+=new
print b

with open('ingredients_from_allrecipes.json', 'w') as outfile:
    json.dump(b,outfile,indent=4)