FROM node:12-alpine3.9 AS builder
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install
COPY . .
ENTRYPOINT ["yarn", "start"]
