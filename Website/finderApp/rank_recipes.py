import csv
import math
from operator import itemgetter
from nltk.corpus import treebank
from nltk import stem

stemmer = stem.PorterStemmer()
dict = {}
indexList = 'finderApp/static/finderApp/data/index_list.csv'
def init(indexList):
	#Read the index_list and store it in python dictionary (dict variable)
	# in format (recipe_number : list_of_ingredients_in_that_recipe)
	input = open(indexList, 'r', newline='')
	reader = csv.reader(input)

	for row in reader:
		list = []
		for i in range(1, len(row)):
			list.append(row[i])
		dict[row[0]] = list
	# End Of loading index_list in a dict
	input.close()

##########################################

# Function that accepts list of ingredients user inputs and as an output it 
# gives a list of touples (recipeNum, number_of_ingredients_that_are_matched_in_a_recipe)
# this function uses global variable dict, you can change it to pass dictionary if you
# want, but I think its more efficient like this

#This function does not take popularity into account! You will have to do that in second step
# for ranking I used number of matches divided by number of ingredients in a recipe
# in this way recipes with huge number of ingredients doesnt always come up
def getSortedRecipes(listOfIngredients):
	init(indexList)
	result = {}
	for (key, recipeListOfIngredients) in dict.items():
		for ingredient in recipeListOfIngredients:
			if ingredient in listOfIngredients:
				if key in result.keys():
					result[key] += 1
				else:
					result[key] = 1
		if key in result.keys():
			result[key] /= len(recipeListOfIngredients)
			result[key] = round(result[key], 2)
	return (sorted(result.items(), key=itemgetter(1), reverse=True))
	
def update(listOfIngredients):
	init(indexList)
	lengthOfDict = len(dict.items())
	list = []
	list.append(lengthOfDict+1)
	for ingredient in listOfIngredients:
		list.append(stemmer.stem(ingredient))
	output = open(indexList, 'a', newline='')
	writer = csv.writer(output)
	writer.writerow(list)
	output.close()
	init(indexList)
	#stemmer.stem(word)

#Example of how to call function
# update(['soy','tea','salt','cheese'])
#print(dict[501])
#print (getSortedRecipes(['soy','tea','salt','cheese']))