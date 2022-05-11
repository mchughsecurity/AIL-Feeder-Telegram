FROM python:3.7-alpine

MAINTAINER adam.mchugh@mchughsecurity.com

WORKDIR /feeder

RUN apk update && apk add ca-certificates && rm -rf /var/cache/apk/*
RUN update-ca-certificates

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./feeder ./

CMD ["python","/feeder/run_feeder.py"]