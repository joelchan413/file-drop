FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
	&& apt-get install -y --no-install-recommends openssl \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/start_https.sh

RUN mkdir -p /app/uploads

EXPOSE 8000

CMD ["/app/start_https.sh"]
