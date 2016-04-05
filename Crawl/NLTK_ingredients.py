import json
import sys
import nltk
from string import digits
from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import treebank


data = json.load(open("ingredient_recipes.json"))

# print data
b = len(data)
a = []
output = []
filtered_word = []
# print b

index = range(0,b)
measure_words = ['cup','cups','teaspoon','tablespoon','ground','kitchen','ounce','cut','pinch','gram','pound','jar','stock','bunch','inch','piece','medium','sub','au','jus','button','container','pot','g','head','bag','box','club','food']

for i in index:
    a = data[i]['ingredients']
    # print a
    a = ','.join(a)
    a = a.replace(",","")
    a = a.replace("/","")
    # print a
    a = ''.join([i for i in a if not i.isdigit()])
    # print a


    tokens = nltk.word_tokenize(a)
    tagged = nltk.pos_tag(tokens)
    nouns = [word for word, pos in tagged if (pos =='NN')]
    nouns_list = [word for word, pos in tagged if (pos =='NN')]
    # downcased = [x.lower() for x in nouns]
    # joind = " ".join(downcased).encode('utf-8')
    # into_string = str(nouns)
    print nouns


    for item in nouns_list:
        if item in measure_words:
            nouns.remove(item)
    output.append(nouns)
    # print output[0][0]


with open('nouns_ingredients_in_each_recipes.json', 'w') as outfile:
    json.dump(output,outfile,indent=4)

