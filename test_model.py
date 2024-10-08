import pandas as pd
import joblib
from keras.models import load_model

# Charger le modèle et le scaler
model = load_model("model_2024-10-08.h5")
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

# Afficher la classe prédite et la probabilité correspondante
print(f"Classe prédite : {predicted_class[0][0]}")
print(f"Probabilité : {prediction[0][0]:.4f}")
