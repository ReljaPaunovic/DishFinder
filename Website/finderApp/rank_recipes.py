import json
import csv
import math
import nltk
from string import digits
from operator import itemgetter
from nltk.corpus import treebank
from nltk import word_tokenize
from nltk import stem
from nltk import pos_tag

dict = {}
stemmer = stem.PorterStemmer()
indexList = 'finderApp/static/finderApp/data/index_list.csv'
listOfIngredientsAll = 'finderApp/static/finderApp/data/TokenizedIngredients.csv'

def init(indexList):
	#Read the index_list and store it in python dictionary (dict variable)
	# in format (recipe_number : list_of_ingredients_in_that_recipe)
	input = open(indexList, 'r', newline='')
	reader = csv.reader(input)

	counter = 0
	for row in reader:
		counter += 1
		list = []
		for i in range(1, len(row)):
			list.append(row[i])
		dict[row[0]] = list
	# End Of loading index_list in a dict

	input.close()
	return counter

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


measure_words = ['cup','cups','teaspoon','tablespoon','ground','kitchen','ounce','cut','pinch',
				'gram','pound','jar','stock','bunch','inch','piece','medium','sub','au','jus',
				'button','container','pot','g','head','bag','box','club','food']
def f(ingredient):
	ingredient = ingredient.replace(",","")
	ingredient = ingredient.replace("/","")
	ingredient = ingredient.replace("-","")
	ingredient = ''.join(i for i in ingredient if not i.isdigit())
	tokens = nltk.word_tokenize(ingredient)
	taggedTokens =  nltk.pos_tag(tokens)
	nouns_list = [word for word, pos in taggedTokens if (pos =='NN')]
	list = []
	for item in nouns_list:
		if item not in measure_words:
			list.append(stemmer.stem(item))
	return list

def updateIndexList(listOfIngredients):
	lengthOfDict = init(indexList)
	in1 = open(listOfIngredientsAll, 'r', newline='')
	r = csv.reader(in1)
	listOfAllIngredients = []
	for item in r:
		listOfAllIngredients.append(item[0])
	# lengthOfDict = len(dict.items()) + 1

	lista = []
	lista.append(lengthOfDict+1)
	for ingredient in listOfIngredients:
		preliminaryList = f(ingredient)
		for item in preliminaryList:
			if item in listOfAllIngredients:
				lista.append(item)
	output = open(indexList, 'a', newline='')
	writer = csv.writer(output)
	writer.writerow(lista)
	output.close()
	in1.close()
	#stemmer.stem(word)

#Example of how to call function
# print(update(['2 ,teaspoons /vanilla extract']))
#update(['soy','tea','salt','cheese'])
#print(dict[501])
#print (getSortedRecipes(['mushroom']))