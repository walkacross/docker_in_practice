# Use an official Python runtime as a parent image
FROM python:3.10.12

RUN pip install pandas==2.1.4 -i https://pypi.douban.com/simple

# Set the current working directory in container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run app.py when the container launches
CMD ["python", "app.py"]
