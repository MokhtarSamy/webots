FROM python:3.9.4-alpine

ENV PACKAGES_DEV="\
    build-base \
    linux-headers \
    "
ENV PIP="\
    sockets\
    requests\
    "
RUN apk add --virtual build-deps $PACKAGES_DEV \
    &&pip install --no-cache-dir $PIP \
    && apk del build-deps \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY mecanismeDeCoordination.py .

ENTRYPOINT ["python3"]
CMD ["mecanismeDeCoordination.py"]
