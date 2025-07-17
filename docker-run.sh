#!/bin/bash

# AI Notes Summarizer - Docker Run Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="ai-notes-summarizer"
TAG="${1:-latest}"
CONTAINER_NAME="ai-notes-summarizer-app"
PORT="${2:-8501}"

echo -e "${BLUE}🚀 Running AI Notes Summarizer Docker Container${NC}"
echo -e "${YELLOW}Image: ${IMAGE_NAME}:${TAG}${NC}"
echo -e "${YELLOW}Port: ${PORT}${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if image exists
if ! docker image inspect "${IMAGE_NAME}:${TAG}" > /dev/null 2>&1; then
    echo -e "${RED}❌ Image ${IMAGE_NAME}:${TAG} not found. Please build it first:${NC}"
    echo -e "${YELLOW}./docker-build.sh${NC}"
    exit 1
fi

# Stop and remove existing container if it exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${YELLOW}🛑 Stopping existing container...${NC}"
    docker stop "${CONTAINER_NAME}" > /dev/null 2>&1 || true
    docker rm "${CONTAINER_NAME}" > /dev/null 2>&1 || true
fi

# Create directories for volumes
mkdir -p logs uploads

# Run the container
echo -e "${BLUE}🐳 Starting container...${NC}"
docker run -d \
    --name "${CONTAINER_NAME}" \
    -p "${PORT}:8501" \
    -v "$(pwd)/logs:/app/logs" \
    -v "$(pwd)/uploads:/app/uploads" \
    -v ai-notes-model-cache:/app/.cache \
    --restart unless-stopped \
    "${IMAGE_NAME}:${TAG}"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Container started successfully!${NC}"
    echo ""
    echo -e "${GREEN}🌐 Application URL: ${YELLOW}http://localhost:${PORT}${NC}"
    echo -e "${GREEN}📊 Container Status:${NC}"
    docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo -e "${BLUE}📝 Useful commands:${NC}"
    echo -e "${YELLOW}View logs: docker logs -f ${CONTAINER_NAME}${NC}"
    echo -e "${YELLOW}Stop container: docker stop ${CONTAINER_NAME}${NC}"
    echo -e "${YELLOW}Remove container: docker rm ${CONTAINER_NAME}${NC}"
else
    echo -e "${RED}❌ Failed to start container!${NC}"
    exit 1
fi
