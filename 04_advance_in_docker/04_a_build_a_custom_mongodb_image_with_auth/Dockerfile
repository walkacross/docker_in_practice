FROM mongo:4.0.0

ENV MONGO_INITDB_ROOT_USERNAME admin-user
ENV MONGO_INITDB_ROOT_PASSWORD admin-password
ENV MONGO_INITDB_DATABASE admin

ADD ./mongo-init.js /docker-entrypoint-initdb.d/
COPY ./mongod.conf /etc/mongod.conf

CMD ["mongod", "--config", "/etc/mongod.conf"]
