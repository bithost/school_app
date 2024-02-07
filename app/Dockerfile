FROM python:3.8-alpine
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
    && \
    rm -rf /var/lib/apt/lists/*
# Specify multiple platforms
# For x86_64
#RUN dpkg --add-architecture amd64
# For arm64
#RUN dpkg --add-architecture arm64
# Define a build argument for the API token
ARG STRAPI_API_TOKEN

# Set the API token as an environment variable
ENV STRAPI_API_TOKEN=$STRAPI_API_TOKEN
WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
