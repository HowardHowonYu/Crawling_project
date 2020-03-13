import pymongo

client = pymongo.MongoClient('mongodb://15.164.136.109:27017')
db = client.job_position_crawler
collection = db.job_position