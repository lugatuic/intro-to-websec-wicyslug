# Use Python
FROM python:3.13

# Update local packages & install ca-certificates to install uv
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
# Install sqlite3
RUN apt install sqlite3
# Install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
# Run installer & remove installer after use
RUN sh /uv-installer.sh && rm /uv-installer.sh
# Ensure uv is in container's path
ENV PATH="/root/.local/bin/:$PATH"

# Set working directory to `app` and copy all files in current dir to container
WORKDIR /app
COPY . .

# Expose port 80 (default for http services)
EXPOSE 80

# Run server as user, not root!
# RUN useradd app
# USER app

CMD ["uv", "run", "app/server.py"]
