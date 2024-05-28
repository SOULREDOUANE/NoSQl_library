from models.book import Book
from services.mongodb_service import MongoDBService
from services.neo4j_service import Neo4jService
import os
import time

def main():
    # MongoDB setup
    mongo_uri = os.getenv('MONGO_URI')
    mongo_db_name = 'user_shopping_list'
    mongodb_service = MongoDBService(mongo_uri, mongo_db_name)
    mongodb_service.connect()

    # Create initial books collection in MongoDB
    books = [
        Book("1984", "George Orwell", "9780451524935", "1949-06-08", 12),
        Book("To Kill a Mockingbird", "Harper Lee", "9780060935467", "1960-07-11", 8),
        Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", "1925-04-10", 5),
        Book("One Hundred Years of Solitude", "Gabriel Garcia Marquez", "9780060883287", "1967-05-30", 7),
        Book("Moby Dick", "Herman Melville", "9781503280786", "1851-10-18", 4)
    ]
    mongodb_service.create_books_collection(books)

    # Neo4j setup
    neo4j_uri = os.getenv('NEO4J_URI')
    neo4j_user = os.getenv('NEO4J_USER')
    neo4j_password = os.getenv('NEO4J_PASSWORD')
    neo4j_service = Neo4jService(neo4j_uri, neo4j_user, neo4j_password)
    neo4j_service.connect()

    # Create initial data in Neo4j
    neo4j_service.create_initial_data(books)

    # Keep the script running
    while True:
        print("Running...")
        time.sleep(60)  # Sleep for 60 seconds

if __name__ == "__main__":
    main()