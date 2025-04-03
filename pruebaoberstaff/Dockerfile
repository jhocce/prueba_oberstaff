
FROM python:3.10-alpine AS Builder
RUN apk update && apk add gcc python3-dev musl-dev linux-headers

ENV PYTHONUNBUFFERED 1

RUN mkdir /api
EXPOSE 8000
WORKDIR /api
COPY . /api/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x ./entry.sh

# CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "apicliente.wsgi:application" ]