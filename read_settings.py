# Python program to read
# json file
  
  
import json
  
# Opening JSON file
f = open('harvesting.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
for i in data['collect_settings']:
    print(i)

print(data.chargetime)
# Closing file
f.close()
