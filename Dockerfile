# Base image with Python and required tools
FROM python:3.10-slim

# Install tmux and curl (for ngrok download)
RUN apt-get update && apt-get install -y \
    tmux \
    curl \
    unzip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Download and install ngrok
RUN curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
	| tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
	&& echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
	| tee /etc/apt/sources.list.d/ngrok.list \
	&& apt update \
	&& apt install ngrok

RUN ngrok config add-authtoken 2u8bAwINn9siwxSNxViliFQyBAx_4RQPsfxcz6RewTgLHuGAh

RUN pip install --no-cache-dir flask dotenv requests 
 
# Set working directory
WORKDIR /app

 # Copy your project files into the container
COPY run.sh .

# Make your bash script executable
RUN chmod +x run.sh

# Expose the Flask port (default 8000)
EXPOSE 8000

# Set the entrypoint to run the script
ENTRYPOINT ["./run.sh"]
