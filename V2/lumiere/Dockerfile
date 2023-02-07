FROM python:3.9.4-alpine

ENV PACKAGES_DEV="\
    build-base \
    linux-headers \
    "
RUN apk add --virtual build-deps $PACKAGES_DEV \
    &&pip install --no-cache-dir sockets \
    && apk del build-deps \
    && rm -rf /var/cache/apk/*

WORKDIR /app

COPY suivreLumieres.py .

ENTRYPOINT ["python3"]
CMD ["suivreLumieres.py"]