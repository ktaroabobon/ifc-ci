FROM continuumio/miniconda3

ENV APP_PATH=/code \
    PYTHONPATH=.
#　開発物のソースコードはcodeデイレクトリ下に配置する

RUN conda create -n ifcci python==3.8

SHELL ["conda", "run", "-n", "ifcci", "/bin/bash", "-c"]
RUN conda install -c conda-forge -c oce -c dlr-sc -c ifcopenshell ifcopenshell

WORKDIR $APP_PATH

EXPOSE 8000