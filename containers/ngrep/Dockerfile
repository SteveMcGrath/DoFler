FROM alpine:3.5

RUN apk add --update --no-cache \
  ngrep

ENV PROJECT_PATH /ngrep

WORKDIR $PROJECT_PATH

CMD ["/usr/bin/ngrep", "-d", "eth1", "-W", "byline", "-qilw", "'get' tcp dst port 80"]