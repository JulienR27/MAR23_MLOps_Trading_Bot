FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y
ADD requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt
ADD src/ src/
WORKDIR /src/app
CMD uvicorn main:api --host 0.0.0.0