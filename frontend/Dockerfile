FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# 构建生产版本
RUN npm run build

EXPOSE 3000

# 使用生产服务器
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]
