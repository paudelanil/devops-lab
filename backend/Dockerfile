FROM python:3.11-slim

WORKDIR /app

# Install netcat for the wait-for-it script
RUN apt-get update && apt-get install -y netcat-openbsd

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh

COPY backend.py .

EXPOSE 8000

CMD ["./wait-for-it.sh", "db", "3306", "uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]