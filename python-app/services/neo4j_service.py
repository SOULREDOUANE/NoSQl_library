from config import neo4j_driver

class Neo4jService:
    def __init__(self):
        self.driver = neo4j_driver

    def create_author(self, author):
        with self.driver.session() as session:
            session.run(
                "CREATE (a:Author {name: $name, birthdate: $birthdate})",
                name=author.name, birthdate=author.birthdate
            )

    def get_author(self, name):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (a:Author {name: $name}) RETURN a",
                name=name
            )
            return result.single()

    def create_book(self, book, author_names):
        with self.driver.session() as session:
            session.run(
                "CREATE (b:Book {title: $title, isbn: $isbn, publication_date: $publication_date})",
                title=book.title, isbn=book.isbn, publication_date=book.publication_date
            )
            for author_name in author_names:
                session.run(
                    "MATCH (b:Book {title: $title}), (a:Author {name: $name}) CREATE (b)-[:WROTE]->(a)",
                    title=book.title, name=author_name
                )

    def get_book(self, title):
        with self.driver.session() as session:
            result = session.run(
                "MATCH (b:Book {title: $title}) RETURN b",
                title=title
            )
            return result.single()

    def update_book(self, title, updates):
        with self.driver.session() as session:
            session.run(
                "MATCH (b:Book {title: $title}) SET b += $updates",
                title=title, updates=updates
            )

    def delete_book(self, title):
        with self.driver.session() as session:
            session.run(
                "MATCH (b:Book {title: $title}) DETACH DELETE b",
                title=title
            )