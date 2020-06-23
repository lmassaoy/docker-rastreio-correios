FROM python:alpine3.7

ARG TZ='America/Sao_Paulo'
ENV DEFAULT_TZ ${TZ}

WORKDIR /app

COPY app.py /app
COPY external_communication /app/external_communication
COPY requirements.txt /app

RUN pip3 install -r requirements.txt
RUN apk upgrade --update \
  && apk add -U tzdata \
  && cp /usr/share/zoneinfo/${DEFAULT_TZ} /etc/localtime \
  && apk del tzdata \
  && rm -rf \
  /var/cache/apk/*

CMD python3 app.py -c $TRACKING_CODE -f $CONSULT_METHOD