# 1 use bind mounts

Bind mounts have been around since the early days of Docker. Bind mounts have limited functionality compared to volumes. When you use a bind mount, a file or directory on the host machine is mounted into a container. The file or directory is referenced by its full or relative path on the host machine. By contrast, when you use a volume, a new directory is created within Docker’s storage directory on the host machine, and Docker manages that directory’s contents.

The file or directory does not need to exist on the Docker host already. It is created on demand if it does not yet exist. Bind mounts are very performant, but they rely on the host machine’s filesystem having a specific directory structure available. If you are developing new Docker applications, consider using named volumes instead. You can’t use Docker CLI commands to directly manage bind mounts.


# 2 start a container with a bind mount
~~~
sudo docker run -d --name divemount --mount type=bind, source=/home/"$(USER)"/temp, target=/app/temp friendlyhello
~~~

# 3 see what happened in /app/temp in container
~~~
sudo docker exec -it divemount bash
~~~

bind directory in host machine into the container
