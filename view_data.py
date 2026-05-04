from database.db import history_collection

print("--- Recent Prompt History in MongoDB ---")
docs = list(history_collection.find().sort("created_at", -1).limit(5))

if not docs:
    print("The database is currently empty. Go generate a prompt in the app first!")
else:
    for doc in docs:
        print(f"\nIdea: {doc.get('raw_idea')}")
        print(f"Category: {doc.get('category')} | Score: {doc.get('score')}")
        print(f"Time: {doc.get('created_at')}")
        print("-" * 40)
