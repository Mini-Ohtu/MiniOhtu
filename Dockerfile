FROM postgres:16-alpine

ENV POSTGRES_USER=admin \
    POSTGRES_PASSWORD=admin \
    POSTGRES_DB=ohtu-db

COPY src/schema.sql /docker-entrypoint-initdb.d/schema.sql