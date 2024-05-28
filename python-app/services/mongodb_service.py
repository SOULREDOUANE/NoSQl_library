from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import time

class MongoDBService:
    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None

    def connect(self, max_retries=5, delay=5):
        for attempt in range(max_retries):
            try:
                self.client = MongoClient(self.uri)
                self.client.admin.command('ping')
                print("MongoDB connection successful")
                self.db = self.client[self.db_name]
                return
            except ConnectionFailure:
                print(f"Attempt {attempt + 1} of {max_retries}: MongoDB service unavailable, retrying in {delay} seconds...")
                time.sleep(delay)
        raise Exception("Failed to connect to MongoDB after multiple attempts")

    def create_books_collection(self, books):
        books_collection = self.db['books']
        books_collection.insert_many([book.to_dict() for book in books])
        print("Initial book authors inserted")