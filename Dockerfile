FROM python:3.7.11-buster

RUN apt-get update && apt-get install -y build-essential gdal-bin
RUN pip install --no-cache-dir wheel
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY . .

# ENTRYPOINT ["python", "manage.py"]
# CMD ["runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--timeout=2", "--bind=0.0.0.0:8000", "thesis_project.wsgi"]
