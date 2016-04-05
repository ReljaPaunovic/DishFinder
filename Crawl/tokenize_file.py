import csv
import json
import sys
import numpy as np

b = json.load(open("ingredients_from_allrecipes_new.json"))
# a = np.loadtxt(r'C:\Users\YiRan\Desktop\Dishfinder\Ingredients\BBC_Ingredients.csv', dtype = str, delimiter = '|',skiprows = 1,usecols = (0,))
c = json.load(open("ingredient_recipes.json"))


d = ''.join(c[0]['ingredients'])
e = ''.join([i for i in d if not i.isdigit()])
f = e.replace("/","").replace("(","").replace(")","")
print d
print e
print f
print b[0]




index = range(0,len(c))

match={}
for i in b:
    find=[]
    for j in index:
        d = ''.join(c[j]['ingredients'])
        e = ''.join([x for x in d if not x.isdigit()])
        f = e.replace("/","").replace("(","").replace(")","")
        if i in f:
            find.append(j)
    match[i]=find
print match
output=[]
output.append(match)
with open('tokenized_ingredients_from_allrecipes.json', 'w') as outfile:
    json.dump(output,outfile,indent=4)








