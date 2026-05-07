from pymongo import MongoClient
import os

# Get Mongo URI from environment (support both names just in case)
MONGO_URI = os.getenv("MONGO_URI") or os.getenv("MONGO_URL")

# ❌ Do NOT fallback to localhost in production
if not MONGO_URI:
    raise ValueError("❌ MONGO_URI is not set in environment variables")

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)

    # Test connection (IMPORTANT)
    client.admin.command('ping')

    db = client["promptgenie_db"]

    print("✅ Connected to MongoDB successfully")

except Exception as e:
    print("❌ MongoDB connection failed:", e)
    raise e


# Collections
users_collection = db["users"]
prompts_collection = db["prompts"]
history_collection = db["prompts_history"]
analytics_collection = db["analytics"]

# Create index safely
try:
    users_collection.create_index("email", unique=True)
    print("✅ Index created for users collection")
except Exception as e:
    print("⚠️ Index creation skipped:", e)