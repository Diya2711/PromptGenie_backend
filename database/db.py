from pymongo import MongoClient
import os

# Get MongoDB URI from environment
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("❌ MONGO_URI is missing")

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection check
    print("✅ MongoDB Connected Successfully")
except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
    raise e

# Select Database
db = client["promptgenie_db"]

# Collections
users_collection = db["users"]
prompts_collection = db["prompts"]
history_collection = db["prompts_history"]
analytics_collection = db["analytics"]

# Create index
try:
    users_collection.create_index("email", unique=True)
except Exception as e:
    print("⚠️ Index creation issue:", e)