import json
import csv
import time
start_time = time.time()

#100-400
i1 = open('Man/EnrichedData_Man.csv', 'r', newline='')
#1 - 300
i2 = open('Manu/EnrichedData.csv', 'r', newline='')
#200-500
i3 = open('Relja/EnrichedData.csv', 'r', newline='')
#1-100 & 300-500
i4 = open('YanHao/EnrichedData_Yanhao.csv', 'r', newline='')
#1-200 & 400-500
i5 = open('Yiran/EnrichedData_Yiran.csv', 'r', newline='')

dict = {}

def fillDict( input ):
	reader = csv.reader(input)
	for row in reader:
		if(row[0] in dict):
			dict[row[0]].append(row[2])
		else:
			list = []
			list.append(row[2])
			dict[row[0]] = list
def findMajority(list):
	temp = {}
	for e in list:
		if e in temp:
			temp[e] += 1
		else:
			temp[e] = 1
	return (max(temp.items()))[0]
			
fillDict(i1)
fillDict(i2)
fillDict(i3)
fillDict(i4)
fillDict(i5)

output = open('votedRecipes.csv', 'w', newline='')
writer = csv.writer(output)

for (key, value) in dict.items():
	row = []
	vote = findMajority(value)
	row.append(key)
	row.append(vote)
	writer.writerow(row)


print("--- %s seconds ---" % (time.time() - start_time))