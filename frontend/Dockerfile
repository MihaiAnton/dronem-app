FROM node:alpine

WORKDIR /usr/app/frontend/
COPY frontend/package*.json ./
RUN npm install -qy
COPY frotnend/ ./
RUN npm run build

CMD ["npm", "start"]