from nltk.corpus import treebank
from nltk import stem
import json
import csv
import time
start_time = time.time()

stemmer = stem.PorterStemmer()

output = open('output.csv', 'w', newline='')
input = open('IngredientsNew.csv', 'r')

reader = csv.reader(input)
writer = csv.writer(output)

for row in reader:
	listOfWords = row[0].split()
	#listOfStemmedWords = []
	for word in listOfWords:
		row[0] = stemmer.stem(word)
		writer.writerow(row)
		
	#writer.writerow(stemmer.stem(word))
	
	#row.append("")
	#row[1] = ' '.join(listOfStemmedWords)
	#writer.writerow(row)


print("--- %s seconds ---" % (time.time() - start_time))