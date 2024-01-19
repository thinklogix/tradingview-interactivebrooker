FROM nginx

# Copy custom Nginx configuration
COPY ./build/config/nginx/default.conf /etc/nginx/conf.d/default.conf