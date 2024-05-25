from neo4j import GraphDatabase

def test_connection(driver):
    with driver.session() as session:
        result = session.run("CALL dbms.components() YIELD name, versions, edition RETURN 'Connected to Neo4j ' + name + ' ' + versions[0] + ' ' + edition AS message")
        print(result.single()["message"])



        
uri = "bolt://localhost:7687"
user = "neo4j"
password = "ragavendra"

driver = GraphDatabase.driver(uri,auth=(user,password))

test_connection(driver)


