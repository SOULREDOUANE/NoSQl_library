from pymongo import MongoClient
from neo4j import GraphDatabase

# MongoDB configuration
MONGO_URI = 'mongodb://localhost:27017'
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client['library']

# Neo4j configuration
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"
neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))