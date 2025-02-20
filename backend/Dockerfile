FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY backend.py backend.py

CMD ["python", "backend.py"]

