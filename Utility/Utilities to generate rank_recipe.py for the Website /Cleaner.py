import json
import csv
import time
start_time = time.time()

destination = open('cleanedRecipes.csv', 'w', )

with open('Recipes.csv', 'r') as source:
	reader = csv.reader(source)
	writer = csv.writer(destination)
	for row in reader:
		if ( row[1].find("nophoto") == -1 and row[1] != ""):
			writer.writerow(row)
		
		
print("--- %s seconds ---" % (time.time() - start_time))