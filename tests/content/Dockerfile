# Dockerfile pour le test Content

# Utiliser l'image de base
FROM python:3.9-slim-buster

# Ajouter le code source et les fichiers de test
ADD content_test.py content_test.py
ADD requirements.txt requirements.txt

# Installer les dépendances
RUN apt-get update && apt-get upgrade
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Ajouter les variables d'environnement nécessaires
ENV API_ADDRESS="localhost"
ENV API_PORT="8000"
ENV LOG="1"

# Lancer le test
CMD ["python3", "content_test.py"]
