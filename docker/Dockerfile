FROM jupyter/minimal-notebook:latest

USER root
WORKDIR /tml
COPY requirements.txt .
RUN pip install -r requirements.txt

# Enable JupyterLab
ENV JUPYTER_ENABLE_LAB=yes

RUN jupyter lab build
RUN jupyter labextension install @jupyter-widgets/jupyterlab-manager

