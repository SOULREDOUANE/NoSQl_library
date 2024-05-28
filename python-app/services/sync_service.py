from services.mongo_service.py import MongoService
from services.neo4j_service.py import Neo4jService

class SyncService:
    def __init__(self):
        self.mongo_service = MongoService()
        self.neo4j_service = Neo4jService()

    def sync_book_to_neo4j(self, book_id):
        book = self.mongo_service.get_book(book_id)
        if book:
            author_ids = book.get('author_ids', [])
            authors = [self.mongo_service.get_author(author_id) for author_id in author_ids]
            author_names = [author['name'] for author in authors if author]
            self.neo4j_service.create_book(book, author_names)

    def sync_author_to_mongo(self, author_name):
        author = self.neo4j_service.get_author(author_name)
        if author:
            author_data = {
                "name": author['name'],
                "birthdate": author['birthdate']
            }
            self.mongo_service.create_author(author_data)
            