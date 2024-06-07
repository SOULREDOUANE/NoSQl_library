from flask import Flask, render_template, request, redirect, url_for
from models.book import Book
from services.mongodb_service import MongoDBService
from services.neo4j_service import Neo4jService
from bson.objectid import ObjectId
import os
from datetime import datetime

app = Flask(__name__)

# MongoDB setup
mongo_uri = os.getenv('MONGO_URI')
mongo_db_name = 'user_shopping_list'
mongodb_service = MongoDBService(mongo_uri, mongo_db_name)
mongodb_service.connect()

# Neo4j setup
neo4j_uri = os.getenv('NEO4J_URI')
neo4j_user = os.getenv('NEO4J_USER')
neo4j_password = os.getenv('NEO4J_PASSWORD')
neo4j_service = Neo4jService(neo4j_uri, neo4j_user, neo4j_password)
neo4j_service.connect()

def insert_sample_books():
    books_collection = mongodb_service.db['books']
    books_collection.drop()  # Drop the existing collection to start fresh
    sample_books = [
        {
            "title": "To Kill a Mockingbird",
            "author_ids": [ObjectId("60d5f2d8a3e2c15b5e1b4f1c"), ObjectId("60d5f2d8a3e2c15b5e1b4f1d")],
            "isbn": "1234567890",
            "publication_date": datetime(2024, 1, 1),
            "copies_available": 5,
            "cover_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/To_Kill_a_Mockingbird_%281963_US_theatrical_poster%29.jpg/440px-To_Kill_a_Mockingbird_%281963_US_theatrical_poster%29.jpg"
        },
        {
            "title": "1984",
            "author_ids": [ObjectId("60d5f2d8a3e2c15b5e1b4f1c")],
            "isbn": "2345678901",
            "publication_date": datetime(2023, 2, 1),
            "copies_available": 3,
            "cover_url": "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1327144697i/3744438.jpg"
        },
        {
            "title": "Pride and Prejudice",
            "author_ids": [ObjectId("60d5f2d8a3e2c15b5e1b4f1d")],
            "isbn": "3456789012",
            "publication_date": datetime(2022, 3, 1),
            "copies_available": 2,
            "cover_url": "https://books.google.co.ma/books/content?id=kQ0mAAAAMAAJ&pg=PP1&img=1&zoom=3&hl=en&bul=1&sig=ACfU3U37zPGoOr2IU2f0PCVIexnC5nPGag&w=1280"
        },
        {
            "title": "The Great Gatsby",
            "author_ids": [ObjectId("60d5f2d8a3e2c15b5e1b4f1c"), ObjectId("60d5f2d8a3e2c15b5e1b4f1d")],
            "isbn": "4567890123",
            "publication_date": datetime(2021, 4, 1),
            "copies_available": 4,
            "cover_url": "https://upload.wikimedia.org/wikipedia/commons/7/7a/The_Great_Gatsby_Cover_1925_Retouched.jpg"
        }
    ]
    books_collection.insert_many(sample_books)


insert_sample_books()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    books = list(mongodb_service.db['books'].find())
    for book in books:
        book['_id'] = str(book['_id'])  # Convert ObjectId to string
    return render_template('books.html', books=books)

@app.route('/authors')
def authors():
    query = "MATCH (a:Author)-[:WROTE]->(b:Book) RETURN a, b"
    result = neo4j_service.driver.session().run(query)
    authors_books = [(record['a']['name'], record['b']['title']) for record in result]
    return render_template('authors.html', authors_books=authors_books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        publication_date = request.form['publication_date']
        copies_available = request.form['copies_available']
        cover_url = request.form['cover_url']
        
        book = Book(title, author, isbn, publication_date, copies_available, cover_url)
        mongodb_service.db['books'].insert_one(book.to_dict())
        neo4j_service.driver.session().run(
            "MERGE (b:Book {title: $title}) MERGE (a:Author {name: $author}) MERGE (a)-[:WROTE]->(b)",
            title=title, author=author
        )
        return redirect(url_for('books'))
    return render_template('add_book.html')

@app.route('/update_book/<book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = mongodb_service.db['books'].find_one({"_id": ObjectId(book_id)})
    if request.method == 'POST':
        updated_data = {
            "title": request.form['title'],
            "author": request.form['author'],
            "isbn": request.form['isbn'],
            "publication_date": request.form['publication_date'],
            "copies_available": request.form['copies_available'],
            "cover_url": request.form['cover_url']
        }
        mongodb_service.db['books'].update_one({"_id": ObjectId(book_id)}, {"$set": updated_data})
        return redirect(url_for('books'))
    return render_template('update_book.html', book=book)

@app.route('/delete_book/<book_id>', methods=['POST'])
def delete_book(book_id):
    mongodb_service.db['books'].delete_one({"_id": ObjectId(book_id)})
    return redirect(url_for('books'))

@app.route('/update_author/<author_name>', methods=['GET', 'POST'])
def update_author(author_name):
    if request.method == 'POST':
        new_name = request.form['new_name']
        query = """
        MATCH (a:Author {name: $author_name})
        SET a.name = $new_name
        """
        neo4j_service.driver.session().run(query, author_name=author_name, new_name=new_name)
        return redirect(url_for('authors'))
    return render_template('update_author.html', author_name=author_name)

@app.route('/delete_author/<author_name>', methods=['POST'])
def delete_author(author_name):
    query = """
    MATCH (a:Author {name: $author_name})-[r:WROTE]->(b:Book) 
    DELETE r, a
    """
    neo4j_service.driver.session().run(query, author_name=author_name)
    return redirect(url_for('authors'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
