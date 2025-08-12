FROM python:3.10-slim
RUN apt-get update && apt-get install -y wget ca-certificates gnupg --no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps chromium
COPY scrape.py .
CMD ["python", "scrape.py"]
