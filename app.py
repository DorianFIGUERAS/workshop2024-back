from flask import Flask, request, jsonify
from keras.models import load_model
from datetime import datetime
from insertion_BDD import insertion_bdd


import numpy as np
import os
import joblib
import pandas as pd


app = Flask(__name__)



current_date = datetime.now().strftime("%Y-%m-%d")
model = load_model(f"model_{current_date}.h5")

@app.route('/data', methods=['POST'])
def processing_data():
    # 1. Vérifier si la requête contient des données JSON
    if not request.is_json:
        return jsonify({"error": "La requête ne contient pas de données JSON."}), 400
    
    # 2. Récupérer les données JSON
    data = request.get_json()
    
    # 3. Extraire les caractéristiques (features) du JSON
    try:
        # Exemple : si ton modèle attend des caractéristiques précises comme 'age', 'bmi', etc.
        features = [
            data['Age'], 
            data['BMI'], 
            data['Glucose'], 
            data['Insulin'], 
            data['HOMA'], 
            data['Leptin'], 
            data['Adiponectin'], 
            data['Resistin'], 
            data['MCP.1']
        ]
    except KeyError as e:
        return jsonify({"error": f"Clé manquante dans les données JSON : {e}"}), 400

    current_date = datetime.now().strftime("%Y-%m-%d")

    # Charger le modèle et le scaler
    model = load_model(f"model_{current_date}.h5")
    scaler = joblib.load("scaler.pkl")

    # Convertir en DataFrame
    df_new = pd.DataFrame([features])

    # Normaliser les nouvelles données avec le scaler sauvegardé
    new_data_scaled = scaler.transform(df_new)

    # Faire une prédiction (la sortie est la probabilité)
    prediction = model.predict(new_data_scaled)

    # Obtenir la classe prédite (0 ou 1)
    predicted_class = (prediction > 0.5).astype("int32")

    # Afficher la classe prédite et la probabilité correspondante
    print(f"Classe prédite : {predicted_class[0][0]}")
    print(f"Probabilité : {prediction[0][0]:.4f}")
    
    if predicted_class[0][0] == 0:
        prediction_text = "Vous ne semblez pas avoir de cancer. Vous pouvez tout de même consulter un médecin pour plus de sécurité."
    else:
        prediction_text = "Vous semblez avoir potentiellement un cancer. Vous pouvez consulter un médecin pour plus de détails et de tests."
    
    insertion_bdd(data['Age'], data['BMI'], data['Glucose'], data['Insulin'], data['HOMA'], data['Leptin'], data['Adiponectin'], data['Resistin'], data['MCP.1'], prediction.tolist())
    # 6. Retourner la prédiction sous forme de JSON
    return jsonify({"prediction": prediction_text, "probabilite": f"prediction[0][0]:.4f"})  # Convertir la prédiction en liste pour JSON

if __name__ == '__main__':
    app.run(debug=True)