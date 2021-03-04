FROM continuumio/miniconda3:4.9.2-alpine

RUN conda install bokeh pandas pyyaml -y
WORKDIR /app
COPY . ./
EXPOSE 5006

CMD ["sh", "-c", "PYTHONPATH=\"${PYTHONPATH}:$(pwd)\" CONFIG_PATH=visualizations/${REGION}.yml bokeh serve --show visualizations/app.py"]
