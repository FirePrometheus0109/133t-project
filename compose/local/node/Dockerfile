FROM node:10.14.0-alpine

RUN apk update && apk upgrade && \
    # karma dependencies
    apk add --no-cache --virtual .build-deps gifsicle pngquant optipng libjpeg-turbo-utils udev ttf-opensans && \
    apk add --no-cache python alpine-sdk chromium-chromedriver chromium xvfb udev yarn bash && \
    npm cache clean --force && \
    rm -rf /var/cache/apk /root/.npm/

ENV DISPLAY=:99 CHROME_BIN=/usr/bin/chromium-browser LIGHTHOUSE_CHROMIUM_PATH=/usr/bin/chromium-browser

COPY ./frontend/package.json ./

## Storing node modules on a separate layer will prevent unnecessary npm installs at each build
RUN npm install && npm install -D && npm install -g @angular/cli && mkdir /app && mv ./node_modules ./app

WORKDIR /app

COPY . .

COPY ./compose/local/node/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

EXPOSE 49153
