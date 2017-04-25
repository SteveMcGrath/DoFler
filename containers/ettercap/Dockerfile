FROM alpine:3.5

RUN apk add --update --no-cache \
  git \
  build-base \
  cmake \
  libpcap \
  libpcap-dev \
  ncurses \
  ncurses-dev \
  libressl \
  libressl-dev \
  zlib-dev \
  curl \
  curl-dev \
  libnet \
  libnet-dev \
  bison \
  flex \
  linux-headers

ENV PROJECT_PATH /ettercap

WORKDIR $PROJECT_PATH

ENV ETTERCAP_VERSION 0.8.2

ADD https://github.com/Ettercap/ettercap/releases/download/v$ETTERCAP_VERSION/ettercap-$ETTERCAP_VERSION.tar.gz ettercap-$ETTERCAP_VERSION.tar.gz

RUN tar -xzf ettercap-$ETTERCAP_VERSION.tar.gz && rm ettercap-$ETTERCAP_VERSION.tar.gz

RUN mkdir $PROJECT_PATH/ettercap-$ETTERCAP_VERSION/build

WORKDIR $PROJECT_PATH/ettercap-$ETTERCAP_VERSION/build

RUN cmake \
   -D ENABLE_GTK=OFF \
   -D CMAKE_INSTALL_PREFIX=/usr \
   -D INSTALL_PREFIX=/usr \
   -D MAN_INSTALLDIR=/usr/share/man \
   -D CMAKE_SKIP_RPATH=ON \
   -D ENABLE_IPV6=yes \
   ../

RUN make

RUN make install

RUN apk del --no-cache \
  git \
  build-base

WORKDIR /

RUN rm -rf $PROJECT_PATH

RUN mkdir $PROJECT_PATH

WORKDIR $PROJECT_PATH

CMD ["/usr/bin/ettercap", "-Tzuqi", "eth1"]