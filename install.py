import os
import rethinkdb as r
import yaml
from models.Results import Results

stream = open(os.getcwd() + "/settings.yml")
settings = yaml.load(stream)

db = settings['db']

print("----------")
print("Installing DB")
r.db_create(settings['db']['name']).run(r.connect(settings['db']['host'], settings['db']['port']))
print("The DB " + settings['db']['name'] + " now exists.")
print("----------")
print("\n")
print("----------")
print("Installing Results")
profile = Results()
profile.createTable()
print("The table now exists")
print("----------")
