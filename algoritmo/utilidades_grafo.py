from neo4j import GraphDatabase

URI = "neo4j+s://1d3d3e94.databases.neo4j.io"
AUTH = ("neo4j", "vm_35vlz7rro0KyZfLEncx_Zzbr-8OJMp8kw5IG1Yww")

def get_driver():
    return GraphDatabase.driver(URI, auth=AUTH)