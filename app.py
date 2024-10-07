from flask import Flask, request, jsonify
from keras.models import load_model
from datetime import datetime
from insertion_BDD import insertion_bdd

import numpy as np

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

    # 4. Convertir les caractéristiques en tableau numpy pour la prédiction
    features_array = np.array([features])  # Le modèle attend une entrée 2D (1, nombre de caractéristiques)

    # 5. Faire la prédiction avec le modèle
    prediction = model.predict(features_array)
    
    insertion_bdd(data['Age'], data['BMI'], data['Glucose'], data['Insulin'], data['HOMA'], data['Leptin'], data['Adiponectin'], data['Resistin'], data['MCP.1'], prediction.tolist())
    # 6. Retourner la prédiction sous forme de JSON
    return jsonify({"prediction": prediction.tolist()})  # Convertir la prédiction en liste pour JSON

if __name__ == '__main__':
    app.run(debug=True)