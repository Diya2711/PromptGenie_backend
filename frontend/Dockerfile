# Use the official Flutter image
FROM cirrusci/flutter:latest

# Set working directory
WORKDIR /app

# Copy pubspec files
COPY frontend/pubspec.* ./

# Get dependencies
RUN flutter pub get

# Copy the rest of the code
COPY frontend/ ./

# Build for web
RUN flutter build web --release --dart-define=API_BASE_URL=$API_BASE_URL

# Use nginx to serve the static files
FROM nginx:alpine
COPY --from=0 /app/build/web /usr/share/nginx/html

# Expose port
EXPOSE 80