FROM debian:11
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install pytest
ADD api_test.py tests_integration/security/api_test.py
WORKDIR /tests_integration/security/
CMD pytest api_test.py