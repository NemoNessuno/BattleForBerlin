FROM node:8 as builder

MAINTAINER Christian Windolf <christianwindolf@web.de>

WORKDIR /app

COPY package.json yarn.lock index.html .babelrc .eslintrc.js .postcssrc.js ./
COPY src/ src/
COPY config/ config/
COPY build/ build/
COPY static/ static/

RUN yarn && yarn build

FROM nginx:1.13

COPY --from=builder /app/dist /usr/share/nginx/html
COPY bfb.conf /etc/nginx/conf.d/default.conf
