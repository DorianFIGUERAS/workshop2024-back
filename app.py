from flask import Flask, request, jsonify
from keras.models import load_model
from datetime import datetime
from insertion_BDD import insertion_bdd


import numpy as np
import os
import joblib
import pandas as pd


app = Flask(__name__)



# Récupérer la liste des noms des modèles dans le dossier models
model_files = [f for f in os.listdir("./models") if f.endswith(".h5")]

# Afficher la liste des modèles
print("Liste des modèles disponibles :")
model_name = []
for model_file in model_files:
    print(model_file)
    model_name.append(model_file)
# Trier les fichiers de modèles par date de modification (du plus récent au plus ancien)
model_files.sort(key=lambda x: os.path.getmtime(os.path.join("./models", x)), reverse=True)

# Récupérer le nom du modèle le plus récent
latest_model_file = model_files[0]
print(f"Le modèle le plus récent est : {latest_model_file}")

# Déterminer la date actuelle pour charger le modèle correspondant
current_date = datetime.now().strftime("%Y%m%d")

# Charger le modèle et le scaler
model = load_model(f"./models/{latest_model_file}")
scaler = joblib.load("scaler.pkl")

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
        region = data['region']
    except KeyError as e:
        return jsonify({"error": f"Clé manquante dans les données JSON : {e}"}), 400

    

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
    
    if 'region' in data:
        doctolib_url = f"https://www.doctolib.fr/oncologue/{region.replace(' ', '-').lower()}"
    else:
        doctolib_url = "https://www.doctolib.fr/oncologue"
    insertion_bdd(data['Age'], data['BMI'], data['Glucose'], data['Insulin'], data['HOMA'], data['Leptin'], data['Adiponectin'], data['Resistin'], data['MCP.1'], prediction.tolist())
    # 6. Retourner la prédiction sous forme de JSON
    return jsonify({"prediction": prediction_text,
                    "probabilite": f"{prediction[0][0]:.4f}",
                    "doctolib_url": doctolib_url
                    })  # Convertir la prédiction en liste pour JSON

if __name__ == '__main__':
    app.run(debug=True)