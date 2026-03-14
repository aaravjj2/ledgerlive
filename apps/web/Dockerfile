# ── LedgerLive Web ── React + Vite → nginx ─────────────────────────
# Stage 1: Build the Vite application
FROM node:22-alpine AS build

WORKDIR /app

# Copy package manifests first for better layer caching
COPY apps/web/package.json apps/web/package-lock.json ./

RUN npm ci --ignore-scripts

# Copy the rest of the frontend source
COPY apps/web/ ./

# Build production bundle (tsc type-check + vite build)
RUN npm run build

# ── Stage 2: Serve with nginx ─────────────────────────────────────
FROM nginx:alpine AS production

# Remove default nginx site
RUN rm -rf /usr/share/nginx/html/* /etc/nginx/conf.d/default.conf

# Copy custom nginx config
COPY apps/web/nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

# ── Healthcheck ───────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
