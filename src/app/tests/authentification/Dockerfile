# Dockerfile pour le test Authentication

# Utiliser l'image de base
FROM python:3.9-slim-buster

# Ajouter le code source et les fichiers de test
COPY authentification_test.py authentification_test.py
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN apt-get update && apt-get upgrade
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Créer le répertoire /logs
RUN mkdir /logs

# # Ajouter les variables d'environnement nécessaires
ENV API_ADDRESS="localhost"
ENV API_PORT="8000"
ENV LOG="1"

# Lancer le test
CMD ["python3", "authentification_test.py"]
