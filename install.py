import os
import rethinkdb as r
import yaml
from models.Results import Results
import time

stream = open(os.getcwd() + "/settings.yml")
settings = yaml.load(stream)

db = settings['db']

# Wait until we have connection to RethinkDB.
print("Try to connect to RethinkDB")
while True:
    try:
        print("...")
        foo = r.connect(settings['db']['host'], settings['db']['port'])
    except r.ReqlDriverError:
        print(r.ReqlDriverError)
        time.sleep(1)
        continue
    break

print("RethinkDB exists.")

print("----------")
print("Installing DB")
print("""
db_name:{}
db_host:{}
db_port:{}
""".format(settings['db']['name'], settings['db']['host'], settings['db']['port']))
try:
    r.db_create(settings['db']['name']).run(r.connect(settings['db']['host'], settings['db']['port']))
except r.ReqlOpFailedError:
    print("DB already exists")
print("The DB " + settings['db']['name'] + " now exists.")
print("----------")
print("\n")
print("----------")
print("Installing Results")
profile = Results()
try:
    profile.createTable()
except r.ReqlOpFailedError:
    print("Table already exists.")
print("The table now exists")
print("----------")
