FROM ubuntu:bionic
ARG DEBIAN_FRONTEND=noninteractive
RUN set -xe \
&& apt-get update -q \
&& apt-get install -y -q \
        python3-pip \
        uwsgi-plugin-python3 \
        ffmpeg
RUN python3 -m pip install firebase-admin speechrecognition
RUN python3 -m pip install requests pydub
RUN python3 -m pip install googletrans==3.1.0a0 words2num
RUN python3 -m pip install flask
RUN mkdir -p /app

COPY ./server/creds/firebase.json .
COPY . /app/
WORKDIR /app/
ENV GOOGLE_APPLICATION_CREDENTIALS=./server/creds/firebase.json
ENTRYPOINT ["/usr/bin/uwsgi", \
            "--master", \
            "--enable-threads", \
            "--die-on-term", \
            "--plugin", "python3"]
CMD ["--http-socket", "0.0.0.0:8000", \
     "--processes", "4", \
     "--chdir", "/app", \
     "--check-static", "static", \
     "--module", "server:app"]