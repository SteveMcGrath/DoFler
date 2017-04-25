FROM alpine:3.5

RUN apk add --update --no-cache \
  git \
  build-base \
  db \
  db-dev \
  libnids \
  libnids-dev \
  libressl \
  libressl-dev \
  libxmu \
  libxmu-dev \
  libnet \
  libnet-dev \
  libpcap \
  libpcap-dev \
  glib-dev \
  portablexdr \
  portablexdr-dev \
  bsd-compat-headers \
  linux-headers

# TODO: Are the linux/bsd-compat headers needed?

ENV PROJECT_PATH /dsniff

WORKDIR $PROJECT_PATH

RUN git clone https://anonscm.debian.org/git/pkg-security/dsniff.git .

COPY patches/* ./patches/

RUN git apply debian/patches/*.patch
RUN git apply --ignore-space-change --ignore-whitespace patches/*.patch

RUN LIBS="$LIBS -lresolv -lglib-2.0 -lgthread-2.0 -lportablexdr" \
    ./configure  \
    --prefix="/usr" \
    --mandir=/usr/share

RUN make

RUN make install

RUN apk del --no-cache \
  git \
  build-base

WORKDIR /

RUN rm -rf $PROJECT_PATH

RUN mkdir $PROJECT_PATH

WORKDIR $PROJECT_PATH

CMD ["/usr/sbin/dsniff", "-i", "eth1"]