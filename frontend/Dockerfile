FROM node:16

WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

RUN npm install --production

# Copy all other files
COPY  public ./public
COPY frontend.js .


CMD ["node", "frontend.js"]