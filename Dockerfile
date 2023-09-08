
# Changed FROM python:3.10-slim to FROM python:3.10-bullseye
# The python:3.10-slim image is based on debian:buster, which is a little bit old. Switched to python:3.10-bullseye, based on debian:bullseye
FROM python:3.10-bullseye

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential && pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "router.main:app", "--host", "0.0.0.0", "--port", "8000"]
