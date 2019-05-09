# Use an official Python runtime as a parent image
FROM python:3.6

RUN pip install pandas==0.24 -i https://pypi.douban.com/simple

# Set the current working directory in container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run app.py when the container launches
CMD ["python", "app.py"]