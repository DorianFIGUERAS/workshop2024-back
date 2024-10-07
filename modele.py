import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from connexion_bdd import requete_bdd
from keras.models import Sequential
from keras.layers import Dense
from keras.models import save_model
from datetime import datetime

# Fonction pour entraîner un modèle IA avec Keras et sauvegarder en .h5
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
    
    # 4. Normaliser les caractéristiques
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # 6. Créer et entraîner un modèle Keras
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Pour un problème de classification binaire
    
    # Compiler le modèle
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Entraîner le modèle
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
    
    # 7. Évaluer le modèle et afficher la précision
    _, accuracy = model.evaluate(X_test, y_test)
    print(f"Précision du modèle : {accuracy * 100:.2f}%")

    # 8. Enregistrer le modèle sous format .h5 avec la date du jour
    current_date = datetime.now().strftime("%Y-%m-%d")
    model_filename = f"model_{current_date}.h5"
    
    save_model(model, model_filename)
    print(f"Modèle enregistré sous le nom : {model_filename}")

    # 9. Retourner le modèle entraîné
    return model

model = train_model_from_mongo(target_column='test2')  # Entraîner le modèle avec les données récupérées
