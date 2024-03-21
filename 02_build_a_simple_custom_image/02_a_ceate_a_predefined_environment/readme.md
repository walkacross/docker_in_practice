# how to build an images
~~~
sudo docker build -t env_with_pandas .
~~~

# run a container
~~~
sudo docker run -dit env_with_pandas
~~~

# dive into the container
~~~
sudo docker exec -it container_id bash
~~~