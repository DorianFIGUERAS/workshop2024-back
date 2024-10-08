from modele import train_model_from_mongo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time

    
def train_model():
    train_model_from_mongo("Classification")
    print('entraînement du modèle terminé')

# Initialiser le scheduler
scheduler = BackgroundScheduler()

# Planifier les tâches
scheduler.add_job(train_model, 'interval', minutes=10080, id='job_entrainement_modele')
print("job_entrainement_modele ajouté")


# Démarrer le scheduler
scheduler.start()

# Pour garder le script en cours d'exécution
try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()