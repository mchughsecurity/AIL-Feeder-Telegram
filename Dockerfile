FROM python:3.8-alpine

MAINTAINER adam.mchugh@mchughsecurity.com

WORKDIR /feeder

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./feeder ./

CMD ["python","/feeder/run_feeder.py"]