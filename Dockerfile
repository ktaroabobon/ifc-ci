FROM python:3.9

ARG DEPLOY_KEY

ENV APP_PATH=/code \
    PYTHONPATH=.

WORKDIR $APP_PATH

RUN apt-get update -y \
    && apt-get upgrade -y

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir poetry &&  \
    rm -rf ~/.cache/pip

COPY . .

RUN poetry install

EXPOSE 8000