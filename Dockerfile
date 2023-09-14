FROM djawad22/guesslang:2.2.1

LABEL maintainer="djawad.dev@gmail.com"

ENV HTTP_PROXY=http://192.168.0.103:1081
ENV HTTPS_PROXY=http://192.168.0.103:1081

WORKDIR /detector

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir -p /data/codes && chmod +x entrypoint.sh

ENTRYPOINT ["/bin/bash", "-c", "/detector/entrypoint.sh"]
