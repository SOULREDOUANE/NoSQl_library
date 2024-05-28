from config import mongo_db

class MongoService:
    def __init__(self):
        self.books = mongo_db['books']
        self.members = mongo_db['members']
        self.loans = mongo_db['loans']
        self.users = mongo_db['users']

    def create_book(self, book):
        return self.books.insert_one(book.__dict__).inserted_id

    def get_book(self, book_id):
        return self.books.find_one({"_id": book_id})

    def update_book(self, book_id, updates):
        self.books.update_one({"_id": book_id}, {"$set": updates})

    def delete_book(self, book_id):
        self.books.delete_one({"_id": book_id})

    def create_member(self, member):
        return self.members.insert_one(member.__dict__).inserted_id

    def get_member(self, member_id):
        return self.members.find_one({"_id": member_id})

    def update_member(self, member_id, updates):
        self.members.update_one({"_id": member_id}, {"$set": updates})

    def delete_member(self, member_id):
        self.members.delete_one({"_id": member_id})

    def create_loan(self, loan):
        return self.loans.insert_one(loan.__dict__).inserted_id

    def get_loan(self, loan_id):
        return self.loans.find_one({"_id": loan_id})

    def update_loan(self, loan_id, updates):
        self.loans.update_one({"_id": loan_id}, {"$set": updates})

    def delete_loan(self, loan_id):
        self.loans.delete_one({"_id": loan_id})

    def create_user(self, user):
        return self.users.insert_one(user.__dict__).inserted_id

    def get_user(self, user_id):
        return self.users.find_one({"_id": user_id})

    def update_user(self, user_id, updates):
        self.users.update_one({"_id": user_id}, {"$set": updates})

    def delete_user(self, user_id):
        self.users.delete_one({"_id": user_id})