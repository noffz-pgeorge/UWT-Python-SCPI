FROM python:3.14.7-slim

WORKDIR /workspaces/UWT-Python-SCPI

RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/workspaces/UWT-Python-SCPI/src
