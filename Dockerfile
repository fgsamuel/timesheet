FROM python:3.10.7-alpine as build
RUN apk add --update --virtual .build-deps \
    build-base \
    postgresql-dev \
    python3-dev \
    libpq
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

FROM python:3.10.7-alpine as main
RUN apk add libpq bash
COPY --from=build /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=build /usr/local/bin/ /usr/local/bin/
COPY --from=build /app/ /app/
WORKDIR /app
ENV PYTHONUNBUFFERED=1
