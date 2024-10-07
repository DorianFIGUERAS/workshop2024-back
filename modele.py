import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # Exemple avec RandomForest
from sklearn.metrics import accuracy_score
from connexion_bdd import requete_bdd
from joblib import dump
from datetime import datetime

# Fonction pour entraîner un modèle IA avec sklearn
def train_model_from_mongo(target_column='test2'):

    data = requete_bdd()

    print("data : ", data)

    # 1. Convertir la liste de documents en DataFrame Pandas
    df = pd.DataFrame(data)
    
    # 2. Vérifier que la colonne cible existe
    if target_column not in df.columns:
        raise ValueError(f"La colonne cible '{target_column}' n'existe pas dans les données.")
    
    # 3. Séparer les caractéristiques (X) et la cible (y)
    X = df.drop(columns=[target_column, '_id'])  # Exclure la colonne '_id' et la colonne cible
    y = df[target_column]  # Cible (label à prédire)
    
    # 4. Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 5. Créer et entraîner un modèle RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 6. Faire des prédictions et calculer la précision
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Précision du modèle : {accuracy * 100:.2f}%")
    
    # 7. Enregistrer le modèle avec la date du jour

    # Obtenir la date actuelle
    current_date = datetime.now().strftime("%Y-%m-%d")
    model_filename = f"model_{current_date}.joblib"

    # Enregistrer le modèle
    dump(model, model_filename)
    print(f"Modèle enregistré sous le nom : {model_filename}")
    # 7. Retourner le modèle entraîné
    return model

model = train_model_from_mongo(target_column='test2')  # Entraîner le modèle avec les données récupérées
