import json
import csv
import time
import os
start_time = time.time()

input = open('tokenized_ingredients_from_BBC_and_allrecipes - FINAL.json', 'r', newline='')
output = open('index_list.csv', 'w', newline='')

data = json.load(input)
dict = {}
for (key, value) in data.items():
	for recipe in value:
		if str(recipe) in dict.keys():
			dict[str(recipe)].append(key)
		else:
			list = []
			list.append(key)
			dict[str(recipe)] = list

#write it into csv for later use
writer = csv.writer(output)
for (key, value) in dict.items():
	list = []
	list.append(key)
	for v in value:
		list.append(v)
	writer.writerow(list)
	

	
print("--- %s seconds ---" % (time.time() - start_time))