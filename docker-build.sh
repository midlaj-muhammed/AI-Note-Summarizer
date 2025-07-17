#!/bin/bash

# AI Notes Summarizer - Docker Build Script
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
DOCKERFILE="${2:-Dockerfile}"

echo -e "${BLUE}🐳 Building AI Notes Summarizer Docker Image${NC}"
echo -e "${YELLOW}Image: ${IMAGE_NAME}:${TAG}${NC}"
echo -e "${YELLOW}Dockerfile: ${DOCKERFILE}${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Build the image
echo -e "${BLUE}📦 Building Docker image...${NC}"
docker build \
    -t "${IMAGE_NAME}:${TAG}" \
    -f "${DOCKERFILE}" \
    --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --build-arg VCS_REF="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')" \
    .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Docker image built successfully!${NC}"
    echo ""
    
    # Show image info
    echo -e "${BLUE}📊 Image Information:${NC}"
    docker images "${IMAGE_NAME}:${TAG}" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    echo ""
    
    echo -e "${GREEN}🚀 To run the container:${NC}"
    echo -e "${YELLOW}docker run -p 8501:8501 ${IMAGE_NAME}:${TAG}${NC}"
    echo ""
    echo -e "${GREEN}🐙 Or use Docker Compose:${NC}"
    echo -e "${YELLOW}docker-compose up${NC}"
else
    echo -e "${RED}❌ Docker build failed!${NC}"
    exit 1
fi
