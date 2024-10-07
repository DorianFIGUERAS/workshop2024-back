from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def requete_bdd():
    # 1. Se connecter à MongoDB
    # Remplacez <username>, <password> et <host> par vos informations MongoDB
    mongo_uri = os.getenv("MONGO_URI")
    client = MongoClient(mongo_uri)

    # 2. Accéder à une base de données spécifique (par exemple, "mydatabase")
    db = client['BreastCancer']

    # 3. Accéder à une collection dans cette base de données (par exemple, "mycollection")
    collection = db['propre']

    # 4. Récupérer tous les documents de la collection
    documents = collection.find()  # Aucun filtre pour récupérer tous les documents

    bdd = []
    # 5. Afficher les colonnes (clés) et les données (valeurs) pour chaque document
    print("Documents dans la collection 'test1':")
    for doc in documents:
        print(doc)  # Affiche chaque document sous forme de dictionnaire
        bdd.append(doc)

    # 6. Fermer la connexion
    client.close()

    return bdd
