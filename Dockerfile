# syntax=docker/dockerfile:1

# docker build -t llm_username:v1 .
# docker run -p 8080:8080 llm_username:v1

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update -y
RUN apt-get install cmake make gcc g++ -y
RUN pip3 install llama-cpp-python

# Install redis
RUN apt-get install -y redis \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8080

CMD sh startup.sh
