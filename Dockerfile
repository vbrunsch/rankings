FROM continuumio/miniconda3:4.9.2-alpine
ENV BOKEH_PY_LOG_LEVEL=info

RUN conda install bokeh pandas pyyaml -y
WORKDIR /visualizations
COPY ./visualizations ./
EXPOSE 5006

CMD ["sh", "-c", "PYTHONPATH=\"${PYTHONPATH}:$(cd ../ && pwd)\" CONFIG_PATH=./config/${REGION}.yml bokeh serve ./ --prefix=${REGION}"]
