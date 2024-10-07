import numpy as np
from keras.models import load_model

# Charger le modèle
model = load_model('model_2024-10-07.h5')

# Créer les données pour la prédiction
# Les données doivent être dans un format NumPy array, avec une forme (1, n_features)
dummy_data = {
    "Age": 48,
    "BMI": 23.5,
    "Glucose": 70,
    "Insulin": 2.7,
    "HOMA": 0.5,
    "Leptin": 8.8,
    "Adiponectin": 9.7,
    "Resistin": 8,
    "MCP-1": 417
}

# Convertir le dictionnaire en tableau NumPy
input_data = np.array([list(dummy_data.values())])

# Vérifier la forme des données (doit être (1, n_features))
print("Forme des données d'entrée :", input_data.shape)

# Effectuer la prédiction
predictions = model.predict(input_data)

print("Prédiction :", predictions)

# # Interprétation du résultat
# threshold = 0.5  # Tu peux ajuster ce seuil selon les besoins
# predicted_class = "Oui" if predictions[0][0] >= threshold else "Non"

# print(f"Prédiction : {predicted_class}, Probabilité : {predictions[0][0]:.2f}")

