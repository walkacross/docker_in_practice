# 0 why use docker

# 1install the docker
~~~
https://docs.docker.com/install/linux/docker-ce/ubuntu/
~~~


# 2use the basic syntax in docker to operate images and container
Image is like a class and container is like a instance of a class

## 2.1 get a image from remote repository
~~~
sudo docker pull hello-world
~~~

list images that was downloaded to your machine
~~~
sudo docker image ls
~~~

## 2.2 get a instance of image, called container
~~~
sudo docker run hello-world
~~~

to see what containers are instanciated
~~~
sudo docker container ls
~~~

## 2.3 dive into the container to see what it is
~~~
sudo docker exec -it container-id bash
~~~


## 2.4  the relationship between image and container
A container is launched by running an image. An image is an executable package that includes everything needed to run an application--the code, a runtime, libraries, environment variables, and configuration files.

A container is a runtime instance of an image--what the image becomes in memory when executed (that is, an image with state, or a user process). You can see a list of your running containers with the command, docker ps, just as you would in Linux.