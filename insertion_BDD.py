from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def insertion_bdd(age, bmi, glucose, insulin, homa, leptin, adiponectin, resistin, mcp1, classification, date, uid=None):
    # 1. Se connecter à MongoDB
    # Remplacez <username>, <password> et <host> par vos informations MongoDB
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)

    # 2. Accéder à une base de données spécifique (par exemple, "mydatabase")
    db = client[os.getenv("DATABASE")]

    # 3. Accéder à une collection dans cette base de données (par exemple, "mycollection")
    collection = db[os.getenv("COLLECTION_USER")]

    # 4. Insérer un document dans la collection
    document = {"Age": age, "BMI": bmi, "Glucose": glucose, "Insulin": insulin, "HOMA":homa, "Leptin":leptin, "Adiponectin":adiponectin, "Resistin":resistin, "MCP-1":mcp1, "Classification": classification, "uid": uid, "date": date}
    insert_result = collection.insert_one(document)
    print(f"Document inséré avec ID : {insert_result.inserted_id}")

    # 6. Fermer la connexion
    client.close()

# insertion_bdd(40, 20, 10, 10, 0.5, 0.5, 0.5, 12, 12, 1, "08-10-2024", uid=None)