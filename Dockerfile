FROM debian:bullseye-slim

RUN apt-get update && \
    apt-get install -y poppler-utils && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN apt-get install -y python3 python3-pip
RUN pip3 install fastapi uvicorn python-multipart

COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]
