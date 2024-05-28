from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import time

def get_database(max_retries=5, delay=5):
    # Provide the MongoDB connection string for the local Docker instance
    CONNECTION_STRING = "mongodb://mongodb:27017"

    for attempt in range(max_retries):
        try:
            # Create a connection using MongoClient
            client = MongoClient(CONNECTION_STRING)
            # Test MongoDB connection
            client.admin.command('ping')
            print("MongoDB connection successful")
            # Return the database
            return client['user_shopping_list']
        except ConnectionFailure:
            print(f"Attempt {attempt + 1} of {max_retries}: MongoDB service unavailable, retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception("Failed to connect to MongoDB after multiple attempts")

def create_initial_books_collection(db):
    # Define the initial data
    books = [
        {"title": "1984", "author": "George Orwell"},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"title": "One Hundred Years of Solitude", "author": "Gabriel Garcia Marquez"},
        {"title": "Moby Dick", "author": "Herman Melville"}
    ]
    
    # Insert initial data into the 'books' collection
    books_collection = db['books']
    books_collection.insert_many(books)
    print("Initial book authors inserted")

if __name__ == "__main__":
    # Get the database
    dbname = get_database()
    
    # Create initial books collection
    create_initial_books_collection(dbname)
    
    # Example usage: print collections in the database
    print("MongoDB collections:", dbname.list_collection_names())

    # Keep the script running
    while True:
        print("Running...")
        time.sleep(60)  # Sleep for 60 seconds