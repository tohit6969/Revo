# Node alpine for minimal footprint
FROM node:18-alpine

WORKDIR /app

# Install JS deps
COPY package.json package-lock.json ./
RUN npm ci

# Copy source
COPY . .

# Expose dev server port
EXPOSE 3000

# Start Next.js or React dev server
CMD ["npm", "run", "dev"]
