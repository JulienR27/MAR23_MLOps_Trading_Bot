FROM debian:11
RUN apt-get update && apt-get install python3-pip -y && apt-get install -y chromium
# && apt-get install -y libnss3 libglib2.0
#RUN apt-get install -y chromium
ADD requirements.txt requirements.txt 
RUN pip3 install -r requirements.txt
ADD src/ src/
WORKDIR /src/app
CMD uvicorn main:api --host 0.0.0.0