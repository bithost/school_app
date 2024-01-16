FROM python:3.8-slim-buster
# Specify multiple platforms
# For x86_64
#RUN dpkg --add-architecture amd64
# For arm64
RUN dpkg --add-architecture arm64

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
