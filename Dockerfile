FROM node:20.4

WORKDIR /homelytics

COPY homelytics/package*.json ./


RUN npm install && npm install vite

COPY . .

CMD ["npm", "run", "dev"]
