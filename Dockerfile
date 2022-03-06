FROM python:3.9-slim-buster

WORKDIR /src

# Install python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app /src/app

CMD ["python", "-m", "app.main"]
