
FROM python:3.10-alpine AS Builder
RUN apk update && apk add gcc python3-dev musl-dev linux-headers

ENV PYTHONUNBUFFERED 1

RUN mkdir /front
EXPOSE 9000
WORKDIR /front
COPY . /front/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# RUN chmod +x ./entry.sh

# CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "apicliente.wsgi:application" ]
# flet run --web --port 8000