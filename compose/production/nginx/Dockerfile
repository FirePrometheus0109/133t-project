# Stage 0, "build-stage", based on Node.js, to build and compile Angular
FROM node:10.14.0 as build-stage

ARG BUILD_ENVIRONMENT

# See https://crbug.com/795759
RUN apt-get update && apt-get install -yq libgconf-2-4
# Install latest chrome dev package and fonts to support major charsets (Chinese, Japanese, Arabic, Hebrew, Thai and a few others)
# Note: this installs the necessary libs to make the bundled version of Chromium that Puppeteer
# installs, work.
RUN apt-get update && apt-get install -y wget --no-install-recommends \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-unstable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst ttf-freefont \
      --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge --auto-remove -y curl \
    && rm -rf /src/*.deb
WORKDIR /app
COPY ./frontend/package*.json /app/
RUN npm install
COPY ./frontend /app/
# RUN npm run test -- --browsers ChromeHeadlessNoSandbox --watch=false
RUN npm run build -- --output-path=./dist/out --configuration ${BUILD_ENVIRONMENT}

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.15

RUN mkdir /app_static
RUN mkdir /app_media

COPY --from=build-stage /app/dist/out/ /usr/share/nginx/html
COPY ./compose/production/nginx/nginx-custom.conf /etc/nginx/conf.d/default.conf
