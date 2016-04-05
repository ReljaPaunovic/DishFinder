import webbrowser
import json
import csv
import time
start_time = time.time()

destination = open('EnrichedData.csv', 'a', newline='')

#Check where did it stop
temp = open('EnrichedData.csv', 'r', newline='')
reader = csv.reader(temp)
alreadyDone = 0
for row in reader:
	alreadyDone += 1

print("*************************************************************************************************")
print("Enter a code for category after each picture, you can stop and start at anytime it will be saved")
print("*************************************************************************************************")
counter = 0
with open('cleanedRecipes.csv', 'r') as source:
	reader = csv.reader(source)
	writer = csv.writer(destination)
	for row in reader:
		counter += 1
		if (counter <= alreadyDone):
			continue
		URL = row[1]
		webbrowser.open(URL)
		print (" Appetiser/Starter = 0 \n Soup              = 1 \n Main Dish         = 2 \n Side Dish         = 3 \n Dessert           = 4 \n Salad             = 5 \n Snack             = 6 \n")
		print("TITLE: " + row[0])
		input_var = input("Enter choice: ")
		row.append(input_var)
		writer.writerow(row)


print("--- %s seconds ---" % (time.time() - start_time))

