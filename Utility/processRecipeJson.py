import json

attributes = ["name", "servings", "image", "category", "contained_ingredients", "directions"]
indentation = "	"

with open('recipe_sample.json') as data_file:    
    data = json.load(data_file)

data_length = len(data)
# preprocess to take care of "\""
for i in range(data_length):
	for j in range(len(attributes)):
		if isinstance(data[i][attributes[j]], list):
			for k in range(len(data[i][attributes[j]])):
				data[i][attributes[j]][k] = data[i][attributes[j]][k].replace("\"", "\\\"")
		else:
			try:
				int(data[i][attributes[j]])
				is_int = True
			except:
				is_int = False
			if not is_int:
				data[i][attributes[j]] = data[i][attributes[j]].replace("\"", "\\\"")

out_file = open("processed_recipe.json", "w")
out_file.write('[\n')

# process data for model: finderApp.Ingredient
ingredient_dic = {}
index = 1
for i in range(data_length):
	ing_length = len(data[i]["contained_ingredients"])
	for j in range(ing_length):
		key = data[i]["contained_ingredients"][j]
		if key not in ingredient_dic:
			ingredient_dic[key] = index
			index = index + 1

for key, value in ingredient_dic.iteritems():
	out_file.write(indentation + '{\n')
	out_file.write(indentation + indentation + '"model": "finderApp.Ingredient",\n')
	out_file.write(indentation + indentation + '"pk": ')
	out_file.write((str)(value) + ',\n')
	out_file.write(indentation + indentation + '"fields": {\n')
	out_file.write(indentation + indentation + indentation + '"ingredient_name": ')
	out_file.write('"' + key + '"\n')
	out_file.write(indentation + indentation + '}\n')
	out_file.write(indentation + '}')
	index = index - 1
	# if index != 1:
	out_file.write(',')
	out_file.write('\n')

# process data for model: finderApp.Direction
direction_dic = {}
index = 1
for i in range(data_length):
	ing_length = len(data[i]["directions"])
	for j in range(ing_length):
		key = data[i]["directions"][j]
		if key not in direction_dic:
			direction_dic[key] = index
			index = index + 1

for key, value in direction_dic.iteritems():
	out_file.write(indentation + '{\n')
	out_file.write(indentation + indentation + '"model": "finderApp.Direction",\n')
	out_file.write(indentation + indentation + '"pk": ')
	out_file.write((str)(value) + ',\n')
	out_file.write(indentation + indentation + '"fields": {\n')
	out_file.write(indentation + indentation + indentation + '"recipe_direction": ')
	out_file.write('"' + key + '"\n')
	out_file.write(indentation + indentation + '}\n')
	out_file.write(indentation + '}')
	index = index - 1
	# if index != 1:
	out_file.write(',')
	out_file.write('\n')

# process data for model: finderApp.Recipe
for i in range(data_length):
	out_file.write(indentation + '{\n')
	out_file.write(indentation + indentation + '"model": "finderApp.Recipe",\n')
	out_file.write(indentation + indentation + '"pk": ')
	out_file.write((str)(data[i]["index"]) + ',\n')
	out_file.write(indentation + indentation + '"fields": {\n')
	for j in range(len(attributes)):
		out_file.write(indentation + indentation + indentation + '"' + attributes[j] + '": ')
		try:
			int(data[i][attributes[j]])
			is_int = True
		except:
			is_int = False
		if is_int:
			# need to increase index by 1 for category field
			if attributes[j] == "category":
				out_file.write((str)(data[i][attributes[j]] + 1))
			else:
				out_file.write((str)(data[i][attributes[j]]))
		else:
			# check if field is "contained_ingredients" or "directions"
			if isinstance(data[i][attributes[j]], list):
				out_file.write('[')
				if attributes[j] == "contained_ingredients":
					for k in range(len(data[i][attributes[j]])):
						out_file.write(str(ingredient_dic[data[i][attributes[j]][k]]))
						if k != (len(data[i][attributes[j]])-1):
							out_file.write(',')
				elif attributes[j] == "directions":
					for k in range(len(data[i][attributes[j]])):
						out_file.write(str(direction_dic[data[i][attributes[j]][k]]))
						if k != (len(data[i][attributes[j]])-1):
							out_file.write(',')
				out_file.write(']')
			else:
				out_file.write('"' + data[i][attributes[j]] + '"')
		if j != (len(attributes)-1):
			out_file.write(',')
		out_file.write("\n")
	out_file.write(indentation + indentation + '}\n')
	out_file.write(indentation + '}')
	if i != (data_length-1):
		out_file.write(',')
	out_file.write('\n')

out_file.write(']')

