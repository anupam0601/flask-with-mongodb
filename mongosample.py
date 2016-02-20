from pymongo import MongoClient 



#mongo = PyMongo(app)
client = MongoClient()
db = client.anupam



items = db.movie.find()
items = [item for item in items]
print items