from flask import Flask, jsonify
from pymongo import MongoClient
from neo4j import GraphDatabase

app = Flask(__name__)

# MongoDB setup
mongo_client = MongoClient('mongodb://mongodb:27017/')
mongo_db = mongo_client['bibliotheque']
books_collection = mongo_db['books']

# Neo4j setup
neo4j_driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "password"))

@app.route('/')
def index():
    return "Welcome to the Library Management System"

@app.route('/books')
def get_books():
    books = list(books_collection.find({}, {"_id": 0}))
    return jsonify(books)

@app.route('/authors')
def get_authors():
    with neo4j_driver.session() as session:
        result = session.run("MATCH (a:Author) RETURN a.name AS name")
        authors = [record["name"] for record in result]
    return jsonify(authors)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
