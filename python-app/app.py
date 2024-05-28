from flask import Flask, request, jsonify
from services.mongo_service import MongoService
from services.neo4j_service import Neo4jService
from services.sync_service import SyncService
from models.book import Book
from models.author import Author
from models.member import Member
from models.loan import Loan
from models.user import User

app = Flask(__name__)

mongo_service = MongoService()
neo4j_service = Neo4jService()
sync_service = SyncService()

# CRUD operations for Books
@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    book = Book(**data)
    book_id = mongo_service.create_book(book)
    sync_service.sync_book_to_neo4j(book_id)
    return jsonify({"book_id": str(book_id)}), 201

@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    book = mongo_service.get_book(book_id)
    return jsonify(book), 200

@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    updates = request.json
    mongo_service.update_book(book_id, updates)
    return jsonify({"message": "Book updated successfully"}), 200

@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    mongo_service.delete_book(book_id)
    return jsonify({"message": "Book deleted successfully"}), 200

# CRUD operations for Authors
@app.route('/authors', methods=['POST'])
def create_author():
    data = request.json
    author = Author(**data)
    neo4j_service.create_author(author)
    sync_service.sync_author_to_mongo(author.name)
    return jsonify({"message": "Author created successfully"}), 201

@app.route('/authors/<name>', methods=['GET'])
def get_author(name):
    author = neo4j_service.get_author(name)
    return jsonify(author), 200

# CRUD operations for Members
@app.route('/members', methods=['POST'])
def create_member():
    data = request.json
    member = Member(**data)
    member_id = mongo_service.create_member(member)
    return jsonify({"member_id": str(member_id)}), 201

@app.route('/members/<member_id>', methods=['GET'])
def get_member(member_id):
    member = mongo_service.get_member(member_id)
    return jsonify(member), 200

@app.route('/members/<member_id>', methods=['PUT'])
def update_member(member_id):
    updates = request.json
    mongo_service.update_member(member_id, updates)
    return jsonify({"message": "Member updated successfully"}), 200

@app.route('/members/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    mongo_service.delete_member(member_id)
    return jsonify({"message": "Member deleted successfully"}), 200

# CRUD operations for Loans
@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.json
    loan = Loan(**data)
    loan_id = mongo_service.create_loan(loan)
    return jsonify({"loan_id": str(loan_id)}), 201

@app.route('/loans/<loan_id>', methods=['GET'])
def get_loan(loan_id):
    loan = mongo_service.get_loan(loan_id)
    return jsonify(loan), 200

@app.route('/loans/<loan_id>', methods=['PUT'])
def update_loan(loan_id):
    updates = request.json
    mongo_service.update_loan(loan_id, updates)
    return jsonify({"message": "Loan updated successfully"}), 200

@app.route('/loans/<loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    mongo_service.delete_loan(loan_id)
    return jsonify({"message": "Loan deleted successfully"}), 200

# CRUD operations for Users
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(**data)
    user_id = mongo_service.create_user(user)
    return jsonify({"user_id": str(user_id)}), 201

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo_service.get_user(user_id)
    return jsonify(user), 200

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    updates = request.json
    mongo_service.update_user(user_id, updates)
    return jsonify({"message": "User updated successfully"}), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    mongo_service.delete_user(user_id)
    return jsonify({"message": "User deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)


