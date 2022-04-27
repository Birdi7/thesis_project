FROM python:3.7.11-buster

RUN apt-get update && apt-get install -y build-essential gdal-bin
RUN pip install --no-cache-dir wheel
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn
# RUN pip uninstall -y mysqlclient
# RUN pip install --no-cache-dir mysql-connector-python==8.0.26

COPY . .

CMD ["gunicorn", "--timeout=50", "--bind=0.0.0.0:80", "thesis_project.wsgi"]
