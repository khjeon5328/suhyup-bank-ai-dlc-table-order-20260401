FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install "bcrypt<5" pymysql

COPY . .

CMD ["python", "-m", "seed.run_seed_standalone"]
