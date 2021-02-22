FROM python:3.7-alpine

# layer caching for faster builds
ADD . /code
COPY requirements.txt /code
RUN apk update && apk add postgresql-dev gcc musl-dev
RUN pip install -r requirements.txt


WORKDIR /code
ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0 --port=5000