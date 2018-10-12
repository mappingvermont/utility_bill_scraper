FROM python:2.7-alpine
MAINTAINER Charlie Hofmann charlie.hofmann@gmail.com

ENV NAME utility_bill_scraper
ENV USER utility_bill_scraper

# install standard python stuff + scrapy dependencies
RUN apk update && apk upgrade && \
   apk add --no-cache --update bash git openssl-dev build-base alpine-sdk \
   libffi-dev gcc python2-dev musl-dev libxslt-dev libxml2-dev 

RUN addgroup $USER && adduser -s /bin/bash -D -G $USER $USER
RUN easy_install pip && pip install --upgrade pip

# copy over requirements.txt and scrapy config
RUN mkdir -p /opt/$NAME
COPY requirements.txt /opt/$NAME/requirements.txt
COPY scrapy.cfg /opt/$NAME/scrapy.cfg

# install
RUN cd /opt/$NAME && pip install -r requirements.txt

# Copy the application folder inside the container
WORKDIR /opt/$NAME
COPY ./$NAME /opt/$NAME/$NAME

