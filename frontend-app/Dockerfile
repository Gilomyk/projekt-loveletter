FROM node:18

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install && yarn add sweetalert2

COPY . .

EXPOSE 5173

CMD ["yarn", "dev"]