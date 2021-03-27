FROM aochenjli/visualizations-base:4.9.2-alpine
ENV BOKEH_PY_LOG_LEVEL=info

WORKDIR /visualizations
COPY ./visualizations ./
EXPOSE 5006

CMD ["sh", "-c", "PYTHONPATH=\"${PYTHONPATH}:$(cd ../ && pwd)\" \
CONFIG_PATH=./config/${REGION}.yml \
LAST_UPDATED_PATH=./last-updated/${REGION} \
bokeh serve ./ --prefix=${REGION}"]
