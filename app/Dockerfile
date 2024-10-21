# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Update and install only necessary dependencies
RUN apk update && \
    apk add --no-cache \
        gcc \
        g++ \
        make \
        libffi-dev \
    && \
    rm -rf /var/cache/apk/*

# Specify multiple platforms
# For x86_64
#RUN dpkg --add-architecture amd64
# For arm64
#RUN dpkg --add-architecture arm64

# Define a build argument for the API token
# ARG STRAPI_API_TOKEN

# # Set the API token as an environment variable
# ENV STRAPI_API_TOKEN=$STRAPI_API_TOKEN

# Create a non-root user and switch to it
RUN adduser -D myuser
USER myuser

# Set the working directory in the container to /app
WORKDIR /app

# Copy only the necessary files
# First, copy only the requirements.txt file to leverage Docker cache
COPY --chown=myuser:myuser requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Remove requirements.txt after installing Python dependencies
RUN rm requirements.txt

# Copy the current directory contents into the container at /app
COPY --chown=myuser:myuser . .

# Run the application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
