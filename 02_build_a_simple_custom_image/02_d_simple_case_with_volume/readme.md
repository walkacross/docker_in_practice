# 1 what and why  volume

~~~
https://docs.docker.com/storage/volumes/
~~~

# 2 create and manage volumes

## 2.1 create a volume
~~~
sudo docker volume create my-vol
~~~

## 2.2 list volumes
~~~
docker run -p 5000:5000 friendlyhello
~~~

## 2.3 inspect a volume:
~~~
sudo docker inspect my-vol
~~~

## 2.4 remove a volume:
~~~
docker volume rm my-vol
~~~

# 3 start a container with a volume
~~~
sudo docker run -d --name divevolume -v myvol2:/app friendlyhello
~~~

## 3.1 inspect the container
~~~
sudo docker inspect divevolume
~~~
you can find the "Mount" info there

## 3.2 enter the container and do something
~~~
sudo docker exec -it divevolume bash

touch helloworld.md
~~~

## 3.3 enter the volume dir to see what happened
~~~
su
cd /var/lib/docker/volume/myvol2/_data
~~~




