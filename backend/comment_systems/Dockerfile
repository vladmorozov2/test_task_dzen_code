FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x wait-for-it.sh

CMD ["sh", "-c", "./wait-for-it.sh db:3306 -t 30 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
