FROM debian:11
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install pytest
ADD predict/api_predict_test.py security/api_security_tests.py tests_integration/
CMD pytest tests_integration/