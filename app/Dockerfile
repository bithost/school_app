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

# Make sure app.py is executable
RUN chmod +x app.py

# Run the application with environment variables
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
