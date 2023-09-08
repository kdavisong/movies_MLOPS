
FROM python:3.10-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

RUN pip install numpy==1.21.4
RUN pip install cython==0.29.24

# Installed the other requirements
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "router.main:app", "--host", "0.0.0.0", "--port", "8000"]
