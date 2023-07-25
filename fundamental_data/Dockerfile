FROM apache/airflow:2.1.2-python3.9
COPY fundamental_data/requirements.txt .
COPY src/domain/utils/fetch_data.py ./src/domain/utils/
COPY src/domain/utils/new_earnings.py ./src/domain/utils/
USER root
RUN apt-get update --fix-missing && pip install -r requirements.txt && apt-get install -y chromium
# RUN apt-get install -y chromium