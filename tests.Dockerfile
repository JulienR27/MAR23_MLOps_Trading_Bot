FROM debian:latest
RUN apt-get update && apt-get install python3-pip -r requirements.txt -y && pip3 install pytest
WORKDIR /app
ADD src/ src/
ADD  app/main.py 
WORKDIR /app
CMD python3 content_test.py