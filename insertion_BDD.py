from pymongo import MongoClient

def insertion_bdd(age, bmi, glucose, insulin, homa, leptin, adiponectin, resistin, mcp1, classification):
    # 1. Se connecter à MongoDB
    # Remplacez <username>, <password> et <host> par vos informations MongoDB
    client = MongoClient("mongodb://admin:password@srv614232.hstgr.cloud:27017/")

    # 2. Accéder à une base de données spécifique (par exemple, "mydatabase")
    db = client['BreastCancer']

    # 3. Accéder à une collection dans cette base de données (par exemple, "mycollection")
    collection = db['test']

    # 4. Insérer un document dans la collection
    document = {"Age": age, "BMI": bmi, "Glucose": glucose, "Insulin": insulin, "HOMA":homa, "Leptin":leptin, "Adiponectin":adiponectin, "Resistin":resistin, "MCP.1":mcp1, "Classification": classification}
    insert_result = collection.insert_one(document)
    print(f"Document inséré avec ID : {insert_result.inserted_id}")

    # 6. Fermer la connexion
    client.close()
