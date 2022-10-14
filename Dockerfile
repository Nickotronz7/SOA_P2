FROM node:16.5-alpine

WORKDIR /my-app

ENV PATH="./node_modules/.bin:$PATH"

COPY ["package*.json","./"]

RUN npm install

COPY . . 

EXPOSE 3000 

CMD ["npm", "start"]
