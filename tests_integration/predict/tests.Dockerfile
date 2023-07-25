FROM debian:11
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install pytest
ADD api_test.py tests_integration/predict/api_predict_test.py
WORKDIR /tests_integration/predict/
CMD pytest api_predict_test.py