FROM python:3.9

ENV APP_PATH=/code \
    PYTHONPATH=.
#　開発物のソースコードはcodeデイレクトリ下に配置する

WORKDIR $APP_PATH

RUN apt-get update && \
    apt-get upgrade -y && \
    pip install poetry


# install python library
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir poetry &&  \
    rm -rf ~/.cache/pip

COPY . .

RUN poetry install

EXPOSE 8000