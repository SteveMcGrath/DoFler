FROM alpine:3.5

RUN apk add --update --no-cache \
  iproute2

WORKDIR /

COPY *.sh ./

CMD ["./span.sh"]
