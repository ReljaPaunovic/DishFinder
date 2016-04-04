
out_file = open("processed_meal.json", "w")

with open("meals.txt") as f:
    content = f.readlines()


indentation = "   "

out_file.write("[\n")
for i in range(len(content)):
	out_file.write(indentation + "{\n")
	out_file.write(indentation + indentation + '"model": "finderApp.Meal",\n')
	out_file.write(indentation + indentation + '"pk": ' + str(i+1) + ',\n')
	out_file.write(indentation + indentation + '"fields": {\n')
	out_file.write(indentation + indentation + indentation + '"suggestion": [')

	indexes = content[i].split()
	index_list = []
	for j in range(len(indexes)):
		if j != len(indexes)-1:
			out_file.write(str(indexes[j]) + ', ')
		else:
			out_file.write(str(indexes[j]))
	out_file.write(']\n')
	out_file.write(indentation + indentation + '}\n')
	out_file.write(indentation + '},\n')

out_file.write("]")



