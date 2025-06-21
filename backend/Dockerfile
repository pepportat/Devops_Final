FROM python:3.11-alpine

WORKDIR /app

RUN apk update && apk add --no-cache \
    gcc \
    g++ \
    libffi-dev \
    musl-dev \
    postgresql-dev \
    python3-dev \
    build-base \
    && rm -rf /var/cache/apk/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]