# Sử dụng Node.js image chính thức từ Docker Hub
FROM node:18-alpine

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file package.json và package-lock.json vào container
COPY package*.json ./

# Cài đặt các dependencies
RUN npm install

# Sao chép tất cả các file từ máy chủ vào container
COPY . .

# Expose port 5173
EXPOSE 5173

# Chạy ứng dụng trong chế độ development với host được mở
CMD ["npm", "run", "dev"]
