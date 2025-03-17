FROM mysql:8.0

COPY init.sql /docker-entrypoint-initdb.d/

ENV MYSQL_ROOT_PASSWORD=password
ENV MYSQL_DATABASE=chat_db

EXPOSE 3306