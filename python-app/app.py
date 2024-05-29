from flask import Flask, render_template, request, redirect, url_for
from models.book import Book
from services.mongodb_service import MongoDBService
from services.neo4j_service import Neo4jService
import os

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    books = mongodb_service.db['books'].find()
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
        
        book = Book(title, author, isbn, publication_date, copies_available)
        mongodb_service.db['books'].insert_one(book.to_dict())
        
        neo4j_service.driver.session().run(
            "MERGE (b:Book {title: $title}) MERGE (a:Author {name: $author}) MERGE (a)-[:WROTE]->(b)",
            title=title, author=author
        )
        
        return redirect(url_for('books'))
    return render_template('add_book.html')

@app.route('/update_book/<book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    book = mongodb_service.db['books'].find_one({"_id": book_id})
    if request.method == 'POST':
        updated_data = {
            "title": request.form['title'],
            "author": request.form['author'],
            "isbn": request.form['isbn'],
            "publication_date": request.form['publication_date'],
            "copies_available": request.form['copies_available']
        }
        mongodb_service.db['books'].update_one({"_id": book_id}, {"$set": updated_data})
        return redirect(url_for('books'))
    return render_template('update_book.html', book=book)

@app.route('/delete_book/<book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    if request.method == 'POST':
        mongodb_service.db['books'].delete_one({"_id": book_id})
        return redirect(url_for('books'))
    book = mongodb_service.db['books'].find_one({"_id": book_id})
    return render_template('delete_book.html', book=book)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)