from dotenv import load_dotenv
load_dotenv()

from database.db import users_collection, history_collection

print("\n==============================")
print("🚀 PROMPTGENIE DATABASE VIEWER")
print("==============================\n")


# =========================================
# 👤 USERS DATA
# =========================================

print("👤 REGISTERED USERS")
print("-" * 40)

users = list(users_collection.find())

if not users:
    print("No users found.\n")
else:
    for user in users:
        print(f"Name       : {user.get('name')}")
        print(f"Email      : {user.get('email')}")
        print(f"Verified   : {user.get('is_verified')}")
        print(f"Created At : {user.get('created_at')}")
        print("-" * 40)


# =========================================
# 🧠 PROMPT HISTORY
# =========================================

print("\n🧠 RECENT PROMPT HISTORY")
print("-" * 40)

docs = list(
    history_collection.find()
    .sort("created_at", -1)
    .limit(10)
)

if not docs:
    print("No prompt history found.")
    print("Generate prompts from frontend/API first.\n")

else:
    for doc in docs:

        print(f"\n💡 Idea      : {doc.get('raw_idea')}")
        print(f"📂 Category  : {doc.get('category')}")
        print(f"⭐ Score      : {doc.get('score')}")
        print(f"🕒 Time       : {doc.get('created_at')}")

        prompts = doc.get("prompts", {})

        print("\n--- Generated Prompts ---")

        print("\n✅ Basic Prompt:")
        print(prompts.get("Basic", "N/A"))

        print("\n🚀 Advanced Prompt:")
        print(prompts.get("Advanced", "N/A"))

        print("\n🛠 Developer Prompt:")
        print(prompts.get("Developer", "N/A"))

        print("\n" + "=" * 50)


print("\n✅ Database check completed successfully.")