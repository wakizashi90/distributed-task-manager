from pymongo import MongoClient


client = MongoClient("mongodb://mongo:27017")
db = client["task_db"]
tasks_collection = db["tasks"]
