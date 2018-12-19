FROM python:3.6
RUN apt-get update

WORKDIR /root
RUN mkdir flask-mongodb-example
COPY ./ ./flask-mongodb-example/
RUN pip install -qr ./flask-mongodb-example/requirements.txt
RUN pip install pymodm
ENV NAME yujiang

ENTRYPOINT ["python", "./flask-mongodb-example/app.py"]
EXPOSE 5000