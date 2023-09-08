
# Changed FROM python:3.10-slim to FROM python:3.10-bullseye
# The python:3.10-slim image is based on debian:buster, which is a little bit old. Switched python to:3.10-bullseye, based on debian:bullseye
FROM python:3.10-bullseye

WORKDIR /app
COPY requirements.txt .
# Added the following line to install the build-essential package required for compiling the Cython files
RUN apt-get update && apt-get install -y build-essential
# Split the pip install command into two separate commands to avoid issues with cython packages
RUN pip install --no-cache-dir numpy==1.21.4 cython==0.29.24
# Installed numpy and cython before installing the other requirements
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "router.main:app", "--host", "0.0.0.0", "--port", "8000"]
