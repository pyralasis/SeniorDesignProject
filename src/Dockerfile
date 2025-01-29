FROM python:3.12-bookworm

RUN mkdir /app
COPY . /app

WORKDIR /app

# install backend dependencies
RUN cd backend && pip install -r requirements.txt

# install frontend dependencies
RUN apt update -qq
RUN apt install -y nodejs npm 
RUN cd frontend && npm install

ENV QUART_DEBUG=1

ENTRYPOINT [ "/bin/bash" ]