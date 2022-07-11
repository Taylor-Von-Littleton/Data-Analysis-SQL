#Set python:3.8 as the base image
FROM python:3.8

#{Dir.pwd}/src /app
COPY 

# Set the working directory to the root of the project
WORKDIR / 

# Install requirements
RUN pip3 install -r requirements.txt 

# Copy the project to the container
COPY . /

# expose port 5000 means that the container will be accessible on port 5000
EXPOSE 5000 

#ENTRYPOINT ["python3"] means that the container will start with python3]
ENTRYPOINT ["python3"]

#CMD [<file_path/file>] means that the container will start with the app.py file]
CMD ["app/app.py"]

