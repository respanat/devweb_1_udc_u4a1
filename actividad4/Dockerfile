# Usa una imagen base de Python ligera)
FROM python:3.9-slim-buster

ENV FLASK_APP=src 
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
