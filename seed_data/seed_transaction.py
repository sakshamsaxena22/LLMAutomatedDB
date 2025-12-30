import os
import random
from datetime import datetime, timedelta, timezone

from pymongo import MongoClient, ASCENDING, DESCENDING
from dotenv import load_dotenv


# -------------------------------------------------
# Load environment variables (.env / system)
# -------------------------------------------------
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise RuntimeError("❌ MONGODB_URI environment variable not set")

# -------------------------------------------------
# MongoDB connection
# -------------------------------------------------
client = MongoClient(MONGODB_URI)
db = client.payments
collection = db.transactions

# -------------------------------------------------
# Create indexes (idempotent)
# -------------------------------------------------
collection.create_index([("timestamp", DESCENDING)])
collection.create_index([("status", ASCENDING)])
collection.create_index([("amount", ASCENDING)])
collection.create_index([("transaction_id", ASCENDING)], unique=True)

# -------------------------------------------------
# Seed configuration
# -------------------------------------------------
TOTAL_RECORDS = 500

STATUSES = ["SUCCESS", "FAILED", "PENDING"]
MERCHANTS = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Uber"]
PAYMENT_METHODS = ["UPI", "CARD", "NETBANKING"]

now_utc = datetime.now(timezone.utc)

documents = []

# -------------------------------------------------
# Generate seed data
# -------------------------------------------------
for i in range(TOTAL_RECORDS):
    documents.append({
        "transaction_id": f"TXN{i:06d}",
        "user_id": f"USER{random.randint(1, 50):03d}",
        "amount": round(random.uniform(100, 20000), 2),
        "currency": "INR",
        "status": random.choice(STATUSES),
        "merchant": random.choice(MERCHANTS),
        "payment_method": random.choice(PAYMENT_METHODS),
        "timestamp": now_utc - timedelta(minutes=random.randint(0, 7 * 24 * 60))
    })

# -------------------------------------------------
# Insert data (ordered=False allows partial success)
# -------------------------------------------------
try:
    result = collection.insert_many(documents, ordered=False)
    print(f"✅ Successfully inserted {len(result.inserted_ids)} transactions")
except Exception as e:
    print("⚠️ Some records may already exist")
    print(str(e))

# -------------------------------------------------
# Final sanity check
# -------------------------------------------------
count = collection.count_documents({})
print(f"📊 Total documents in collection: {count}")
