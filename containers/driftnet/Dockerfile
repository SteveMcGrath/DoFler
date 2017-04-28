FROM node:6.10-alpine

RUN apk add --update --no-cache \
  git \
  build-base \
  libpcap \
  libpcap-dev

ENV PROJECT_PATH /driftnet

WORKDIR $PROJECT_PATH

RUN git clone https://github.com/bldewolf/driftnet.git .

RUN sed -i 's/#CFLAGS += -DNO_DISPLAY_WINDOW/CFLAGS += -DNO_DISPLAY_WINDOW/g' Makefile
RUN sed -i 's/CFLAGS  += `pkg-config --cflags gtk+-2.0` `pkg-config --cflags libpng`/#CFLAGS  += `pkg-config --cflags gtk+-2.0` `pkg-config --cflags libpng`/g' Makefile
RUN sed -i 's/LDLIBS  += -ljpeg -lgif `pkg-config --libs gtk+-2.0` `pkg-config --libs libpng`/#LDLIBS  += -ljpeg -lgif `pkg-config --libs gtk+-2.0` `pkg-config --libs libpng`/g' Makefile

RUN make

RUN cp driftnet /usr/bin

RUN apk del --no-cache \
  git \
  build-base

WORKDIR /

RUN rm -rf $PROJECT_PATH

RUN mkdir $PROJECT_PATH

WORKDIR $PROJECT_PATH

COPY app .

RUN npm install # Install dev dependencies so that we can run gulp

RUN ./node_modules/.bin/gulp build # Run tests and linting

RUN rm -rf node_modules # Clear out node_modules

RUN npm install --production # Only install the production dependencies

CMD ["node", "./index.js"]
