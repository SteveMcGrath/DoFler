FROM fish/docker-spotter

RUN apk add --update --no-cache \
  iproute2 \
  docker

WORKDIR /

COPY . .

ENTRYPOINT ["./network_manager"]
