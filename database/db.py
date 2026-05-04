from pymongo import MongoClient
import os

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["promptgenie_db"]

# Collections
users_collection = db["users"]
prompts_collection = db["prompts"]
history_collection = db["history"]
analytics_collection = db["analytics"]
users_collection.create_index("email", unique=True)
