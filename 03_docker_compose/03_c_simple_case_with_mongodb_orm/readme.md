# 1docker-compose make multi container reachable

## 1.1  write syntax to mount a directory to a container by volume
~~~
see docker-compose.yml
~~~

## 1.2 run your image
~~~
docker-compose up
~~~

see your mount directory

## 1.3 inspect the container
~~~
sudo docker inspect mongodb_container_id
~~~

check its netwotk info
~~~
IPAddress: blablabla
~~~

## 1.4 access mongodb container from external
~~~
use robot to connect, and check database and documents
~~~
