FROM continuumio/anaconda3

ENV APP_PATH=/code \
    PYTHONPATH=.
#　開発物のソースコードはcodeデイレクトリ下に配置する

RUN conda create -n ifcci python=3.8

RUN /bin/bash -c ". activate ifcci" && \
    conda install -c conda-forge -c oce -c dlr-sc -c ifcopenshell ifcopenshell && \

WORKDIR $APP_PATH

RUN pip install poetry

COPY . .

RUN poetry install
#　必要なパッケージ等をインストールする

EXPOSE 8000