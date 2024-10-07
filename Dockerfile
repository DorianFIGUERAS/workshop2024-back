# Utiliser une image de base officielle Python
FROM python:3.11.5

# Créer un utilisateur non-root
RUN useradd -ms /bin/sh -u 1001 appuser

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt requirements.txt

# Changer les permissions pour permettre à l'utilisateur non-root de lire les fichiers
RUN chown appuser:appuser /app

# Installer les dépendances en tant qu'utilisateur root
USER root
RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Installer supervisord
RUN apt-get update && \
    apt-get install -y supervisor && \
    apt-get clean

# Copier le fichier de configuration de supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copier le reste de l'application et changer les permissions
COPY . .
RUN chown -R appuser:appuser /app

# Créer les répertoires de logs nécessaires et définir les permissions
RUN mkdir -p /var/log/supervisor && \
    chown -R appuser:appuser /var/log/supervisor

# Exposer le port utilisé par votre application Flask
EXPOSE 8000

# Définir le fuseau horaire
ENV TZ=Europe/Paris

# Passer à l'utilisateur root pour démarrer supervisord
USER root

# Démarrer supervisord
CMD ["supervisord", "-n"]