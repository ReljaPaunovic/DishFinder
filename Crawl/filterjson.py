import json

# with open('recipes.json', 'w') as source:
data = json.load(open("500_ingredients_with_index_catergory.json"))
    # for element in data: 
    #     del element['rating']
for item in data:
    # if data[i]["author"] == "My review":
        # item = data[i]["rating"]
        item.pop('rating')
        item.pop('author')
        item.pop('directions')
        item.pop('name')
        item.pop('url')
        item.pop('images')
        item.pop('servings')
        # break

# Output the updated file with pretty JSON                                      
open("ingredient_recipes.json", "w").write(
    json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
)

# str_response = response.readall().decode('source')
# data = json.loads(str_response)

# destination = open('recipes.json', 'a', newline='')
# temp = open('recipes.json', 'r', newline='')
# reader = json.reader(temp)

# with open('cleanedRecipes.json', 'r') as source:
#     reader = json.reader(source)
#     writer = json.writer(destination)