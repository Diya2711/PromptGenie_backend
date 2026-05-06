from pymongo import MongoClient
import os

# Get Mongo URI from environment
MONGO_URI = os.getenv("MONGO_URI")

# Safe fallback (prevents crash)
if not MONGO_URI:
    print("⚠️ WARNING: MONGO_URI not found, using fallback")
    MONGO_URI = "mongodb://localhost:27017"

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client["promptgenie_db"]
    print("✅ Connected to MongoDB")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
    raise e

# Collections
users_collection = db["users"]
prompts_collection = db["prompts"]
history_collection = db["prompts_history"]
analytics_collection = db["analytics"]

# Index
users_collection.create_index("email", unique=True)