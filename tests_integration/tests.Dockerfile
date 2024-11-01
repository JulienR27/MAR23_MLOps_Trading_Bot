FROM debian:11
RUN apt-get update && apt-get install python3-pip -y && pip3 install requests && pip3 install pytest
ADD tests_integration/ tests_integration/
CMD pytest tests_integration/