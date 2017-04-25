FROM alpine:3.5

RUN apk add --update --no-cache \
  tshark \
  wireshark-common

ENV PROJECT_PATH /tshark

WORKDIR $PROJECT_PATH

COPY bin /bin

CMD ["tshark.sh"]