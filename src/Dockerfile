# Utilisez une image de base appropriée pour votre application Python
FROM python:3.9

# Copiez les fichiers de votre application dans l'image Docker
COPY . /app

# Définissez le répertoire de travail
WORKDIR /app

# Installez les dépendances de votre application
RUN pip install -r requirements.txt

# Exposez le port sur lequel votre application écoute
EXPOSE 8000

# Démarrez votre application lors du démarrage du conteneur
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]
