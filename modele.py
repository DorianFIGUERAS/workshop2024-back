import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from connexion_bdd import requete_bdd
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.models import save_model
from datetime import datetime
from keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import joblib  # Pour sauvegarder le scaler

# Fonction pour entraîner un modèle IA avec Keras et sauvegarder en .h5
def train_model_from_mongo(target_column):

    # Récupérer les données depuis la BDD
    data = requete_bdd()

    # 1. Convertir la liste de documents en DataFrame Pandas
    df = pd.DataFrame(data)

    print("df", df)

    # 2. Vérifier que la colonne cible existe
    if target_column not in df.columns:
        raise ValueError(f"La colonne cible '{target_column}' n'existe pas dans les données.")
    
    # 3. Séparer les caractéristiques (X) et la cible (y)
    X = df.drop(columns=[target_column, '_id'])  # Exclure la colonne '_id' et la colonne cible
    y = df[target_column]  # Cible (label à prédire)
    
    # 4. Normaliser les caractéristiques
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Sauvegarder le scaler pour utilisation future
    scaler_filename = "scaler.pkl"
    joblib.dump(scaler, scaler_filename)
    print(f"Scaler sauvegardé sous le nom : {scaler_filename}")

    # 5. Diviser les données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # 6. Créer et entraîner un modèle Keras amélioré
    model = Sequential()
    model.add(Dense(128, input_dim=X_train.shape[1], activation='relu'))  # Couches plus larges
    model.add(Dropout(0.3))  # Ajout d'un dropout pour éviter l'overfitting
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))  # Un autre Dropout
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Pour un problème de classification binaire
    
    # Compiler le modèle
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Entraîner le modèle
    # Définir un callback pour l'arrêt anticipé
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # Entraîner le modèle avec l'arrêt anticipé
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test), callbacks=[early_stopping])  # Augmentation des epochs
    plt.plot(history.history['loss'], label='Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.show()
    
    # 7. Évaluer le modèle et afficher la précision
    _, accuracy = model.evaluate(X_test, y_test)
    print(f"Précision du modèle : {accuracy * 100:.2f}%")

    # 8. Prédire les valeurs de test et afficher la matrice de confusion
    y_pred = (model.predict(X_test) > 0.5).astype("int32")  # Seuil de 0.5 pour classification binaire
    cm = confusion_matrix(y_test, y_pred)

    # Afficher la matrice de confusion
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap=plt.cm.Blues)
    plt.show()

    # 9. Enregistrer le modèle sous format .h5 avec la date du jour
    current_date = datetime.now().strftime("%Y-%m-%d")
    model_filename = f"./models/model_{current_date}.h5"
    
    save_model(model, model_filename)
    print(f"Modèle enregistré sous le nom : {model_filename}")
    
    # 10. Retourner le modèle entraîné
    return model

# Entraîner le modèle avec la colonne cible 'Classification'
# model = train_model_from_mongo(target_column='Classification')
