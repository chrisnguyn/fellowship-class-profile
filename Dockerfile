FROM python:3.7-alpine

ARG PORT
ARG WORKERS

WORKDIR /web

COPY requirements.txt requirements.txt

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r requirements.txt

COPY . .

ENV PORT ${PORT}
ENV WORKERS ${WORKERS}

EXPOSE ${PORT}

CMD gunicorn -w ${WORKERS} -b 0.0.0.0:${PORT} web:app --reload
