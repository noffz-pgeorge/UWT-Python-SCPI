FROM python:3.14.7-slim

RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

# Non-root user for the dev container. Dev Containers changes its UID to match
# your WSL user at startup, so files created in the workspace are owned by you.
ARG USERNAME=vscode
RUN useradd -m -s /bin/bash "$USERNAME"