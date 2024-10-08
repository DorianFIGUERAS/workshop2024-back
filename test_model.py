import pandas as pd
import joblib
from keras.models import load_model
from datetime import datetime
import os

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

# Exemple de nouvelles données
new_data = {
    "Age": 51,
    "BMI": 18.37,
    "Glucose": 105,
    "Insulin": 6.03,
    "HOMA": 1.57,
    "Leptin": 9.62,
    "Adiponectin": 12.76,
    "Resistin": 3.21,
    "MCP-1": 513.66
}

# Convertir en DataFrame
df_new = pd.DataFrame([new_data])

# Normaliser les nouvelles données avec le scaler sauvegardé
new_data_scaled = scaler.transform(df_new)

# Faire une prédiction (la sortie est la probabilité)
prediction = model.predict(new_data_scaled)

# Obtenir la classe prédite (0 ou 1)
predicted_class = (prediction > 0.5).astype("int32")

pourcentage_prediction = round(100 * float(f"{prediction[0][0]:.4f}"), 1)
# Afficher la classe prédite et la probabilité correspondante
print(f"Classe prédite : {predicted_class[0][0]}")
print(f"Probabilité : {pourcentage_prediction} %")
