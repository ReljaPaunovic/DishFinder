import json
import numpy as np

data = json.load(open("findback_recipes.json"))
b = np.loadtxt(r'C:\Users\YiRan\Desktop\Dishfinder\Ingredients\votedRecipes-backup.csv', dtype = str, delimiter = '|',skiprows = 1,usecols = (0,))


# print data[1]
# # c = b[0].replace(",","")
# print b[0]

# d = int(filter(str.isdigit, b[0].replace(",","")))
# print d


i = 0
for each in data:
	each['index'] = i
	if i == 0:
	    each['catogery'] = 4
	else:
		each['catogery'] = int(filter(str.isdigit, b[i-1].replace(",","")))
	i+=1

print data

with open('500_ingredients_with_index_catergory.json', 'w') as outfile:
    json.dump(data,outfile,indent=4)