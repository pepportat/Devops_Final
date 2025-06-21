FROM python:3.11-alpine

WORKDIR /app

RUN apk update && apk add \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]