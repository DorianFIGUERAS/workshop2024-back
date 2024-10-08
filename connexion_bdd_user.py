from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def requete_bdd_user(uid=None):
    # 1. Se connecter à MongoDB
    # Remplacez <username>, <password> et <host> par vos informations MongoDB
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)

    # 2. Accéder à une base de données spécifique (par exemple, "mydatabase")
    db = client['BreastCancer']

    # 3. Accéder à une collection dans cette base de données (par exemple, "mycollection")
    collection = db[os.getenv("COLLECTION_USER")]

    query ={}

    if uid!="" and uid!=None:
        query = {"uid": uid}


        projection = {"_id": 0}

        # 4. Récupérer tous les documents de la collection
        documents = collection.find(query, projection)  # Aucun filtre pour récupérer tous les documents

        bdd = []
        # 5. Afficher les colonnes (clés) et les données (valeurs) pour chaque document
        print(f"Documents dans la collection pour uid = {uid}:")
        for doc in documents:
            print(doc)  # Affiche chaque document sous forme de dictionnaire
            bdd.append(doc)
    else:
        bdd = ["Pas de résultat"]

    # 6. Fermer la connexion
    client.close()

    return bdd

# requete_bdd(uid="123")