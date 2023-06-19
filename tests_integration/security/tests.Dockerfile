FROM debian:latest
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install pytest
ADD tests/app/api_test.py app/api_test.py
WORKDIR /app
CMD pytest api_test.py