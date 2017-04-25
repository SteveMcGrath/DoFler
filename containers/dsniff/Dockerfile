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
#  libtirpc-dev \
  portablexdr \
  portablexdr-dev \
  bsd-compat-headers \
  linux-headers

ENV PROJECT_PATH /dsniff

WORKDIR $PROJECT_PATH

RUN git clone https://anonscm.debian.org/git/pkg-security/dsniff.git .

COPY patches/* ./patches/

RUN git apply debian/patches/*.patch
RUN git apply --ignore-space-change --ignore-whitespace patches/*.patch

RUN LDFLAGS="-lresolv -lglib-2.0 -lgthread-2.0 -lportablexdr $LDFLAGS" \
    ./configure  \
    --prefix="/usr" \
    --mandir=/usr/share

RUN make

RUN make install

RUN ls

#RUN cp dsniff /usr/bin

RUN apk del --no-cache \
  git \
  build-base

WORKDIR /

RUN rm -rf $PROJECT_PATH

RUN mkdir $PROJECT_PATH

WORKDIR $PROJECT_PATH

CMD ["/usr/bin/dsniff", "-i", "eth1"]