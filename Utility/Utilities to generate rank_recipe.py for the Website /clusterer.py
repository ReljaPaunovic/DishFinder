import json
import csv
import time
import math
import random
#from scipy.spatial import distance

start_time = time.time()

dict = {}
input = open('index_list.csv', 'r', newline='')
reader = csv.reader(input)

tokenized_ingedients = open('tokenized_ingredients_from_BBC_and_allrecipes.json', 'r', newline='')
data = json.load(tokenized_ingedients)
ingredients = list(data.keys())
length = len(ingredients)

for row in reader:
	list = []
	for i in range(1, len(row)):
		list.append(row[i])
	dict[row[0]] = list

for (key, value) in dict.items():
	list = []
	for i in range(0, length):
		if ingredients[i] in value:
			list.append(1)
		else:
			list.append(0)
	dict[key] = list
	
#From this point, dict contains vectors for each recipe with 1 if ingredient is present or 0 if not
#Appetiser/Starter = 0 
#Soup = 1
#Main Dish = 2
#Side Dish= 3
#Dessert= 4
#Salad = 5 

# Spliting
jsonFile = open('500_ingredients_with_index_catergory.json', 'r')
data = json.load(jsonFile)

appetiser = {}
mainDish = {}
sideDish = {}

for (key, value) in dict.items():
	for dish in data:
		if(dish['catogery'] == 0 and dish['index'] == int(key)):
			appetiser[key] = value
		elif(dish['catogery'] == 2 and dish['index'] == int(key)):
			mainDish[key] = value
		elif(dish['catogery'] == 3 and dish['index'] == int(key)):
			sideDish[key] = value
			


#################################################
appetiserCluster = {}
mainDishCluster = {}
sideDishCluster = {}


def distance(a, b):
	length = len(a)
	sum = 0
	for i in range(0,length):
		sum += (a[i] - b[i])*(a[i] - b[i])
	return (math.sqrt(sum)*1.0/math.sqrt(length)*1.0)

def clusterer(recnik, treshold, resulting_dictionary):
	clusterNum = 1
	for (recipe, array) in recnik.items():
		if recipe not in resulting_dictionary:
			resulting_dictionary[recipe] = clusterNum
			for (otherRecipe, otherArray) in recnik.items():
				if otherRecipe not in resulting_dictionary:
					dist = distance(array, otherArray)
					if (dist <= treshold):
						resulting_dictionary[otherRecipe] = clusterNum
			clusterNum += 1
	
clusterer(appetiser, 0.182222222222222222,appetiserCluster)
clusterer(mainDish, 0.200000000000002, mainDishCluster)
clusterer(sideDish, 0.2200000000000002, sideDishCluster)

#combine

def takeRandomRepresentativeFromCluster(dict, clusterNum):
	masterList = []
	
	for (key, value) in dict.items():
		if(value == clusterNum):
			masterList.append(key)
	#print(masterList)
	return random.choice(masterList)
		
output = open('meals.csv', 'a', newline='')
writer = csv.writer(output)

print(max(appetiserCluster.values()))
print(max(mainDishCluster.values()))
print(max(sideDishCluster.values()))

for i in range(1, max(appetiserCluster.values()) + 1):
	for j in range(1, max(mainDishCluster.values()) + 1):
		for k in range(1, max(sideDishCluster.values()) + 1):
			list = []
			#print("\n \n \n \n")
			first = takeRandomRepresentativeFromCluster(appetiserCluster, i)
			second = takeRandomRepresentativeFromCluster(mainDishCluster, j)
			third = takeRandomRepresentativeFromCluster(sideDishCluster, k)
			list.append(first)
			list.append(second)
			list.append(third)
			writer.writerow(list)

output.close()
#print(resulting_dictionary)
print('\n')
#print(resulting_dictionary.values())
print('\n')
#print(max(resulting_dictionary.values()))



print("--- %s seconds ---" % (time.time() - start_time))