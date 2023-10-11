FROM apache/airflow:2.7.1
RUN pip install --upgrade pip
RUN pip install pika==1.3.2