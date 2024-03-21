# build a totally custom mongodb image with auth

## step 1: docker build
~~~
sudo docker build --tag mongo-auth .
~~~

## step 2: docker run
~~~
sudo docker run --name mongo-auth-instance mongo-auth
~~~

## step 3: docker exec
~~~
sudo docker exec -it mongo-auth-instance bash
mongo
use admin
db.auth("admin-user","admin=password") // has already created
~~~


## step 4: connect the database with rebomongo
~~~
~~~
