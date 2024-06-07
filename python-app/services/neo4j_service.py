from neo4j import GraphDatabase

class Neo4jService:
    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver = None

    def connect(self):
        print(f"Connecting to Neo4j with URI: {self.uri}, User: {self.user}")
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def create_initial_data(self, books):
        with self.driver.session() as session:
            session.run("CREATE CONSTRAINT FOR (b:Book) REQUIRE b.title IS UNIQUE")
            session.run("CREATE CONSTRAINT FOR (a:Author) REQUIRE a.name IS UNIQUE")

            for book in books:
                session.run("MERGE (b:Book {title: $title}) MERGE (a:Author {name: $author}) MERGE (a)-[:WROTE]->(b)",
                            title=book.title, author=book.author)
            print("Initial Neo4j data inserted")