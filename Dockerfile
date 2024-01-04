FROM python:3.10
#COPY ./Nethereum.Docs/ /Nethereum.Docs/
#WORKDIR /Nethereum.Docs/
RUN pip install mkdocs
EXPOSE 8080
CMD ["mkdocs", "serve"]
