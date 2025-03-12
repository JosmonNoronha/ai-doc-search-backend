from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

# MongoDB Atlas Connection
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "pdfscanner"  # Ensure this matches your MongoDB cluster database name

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
documents_collection = db["codewizards"]  # Collection to store uploaded documents




collection = db["codewizards"]

async def get_document_by_id(doc_id: str):
    try:
        from bson import ObjectId
        object_id = ObjectId(doc_id)

        print("Checking MongoDB connection...")
        if collection is None:  # ✅ Correct way to check if collection is None
            print("MongoDB collection is None!")
            return None

        doc = await collection.find_one({"_id": object_id})
        print(f"Document retrieved: {doc}")
        return doc

    except Exception as e:
        print(f"Error fetching document: {e}")
        return None



