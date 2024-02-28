FROM ghcr.io/deephaven/web-plugin-packager:latest as js-plugins
RUN ./pack-plugins.sh @deephaven/js-plugin-ui

FROM ghcr.io/deephaven/server:0.33.1
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install --no-cache-dir --only-binary=:all: deephaven-plugin-ui
COPY uris.csv /uris.csv
COPY config /opt/deephaven/config
COPY --from=js-plugins js-plugins/ /opt/deephaven/config/js-plugins/
