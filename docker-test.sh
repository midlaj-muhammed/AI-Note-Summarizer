#!/bin/bash

# AI Notes Summarizer - Docker Test Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="ai-notes-summarizer"
TAG="test"
CONTAINER_NAME="ai-notes-summarizer-test"
TEST_PORT="8502"

echo -e "${BLUE}🧪 Testing AI Notes Summarizer Docker Setup${NC}"
echo ""

# Function to cleanup
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up test resources...${NC}"
    docker stop "${CONTAINER_NAME}" > /dev/null 2>&1 || true
    docker rm "${CONTAINER_NAME}" > /dev/null 2>&1 || true
    docker rmi "${IMAGE_NAME}:${TAG}" > /dev/null 2>&1 || true
}

# Trap cleanup on exit
trap cleanup EXIT

# Test 1: Build the Docker image
echo -e "${BLUE}📦 Test 1: Building Docker image...${NC}"
if docker build -t "${IMAGE_NAME}:${TAG}" .; then
    echo -e "${GREEN}✅ Docker build successful${NC}"
else
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
fi

# Test 2: Check image size
echo -e "${BLUE}📊 Test 2: Checking image size...${NC}"
IMAGE_SIZE=$(docker images "${IMAGE_NAME}:${TAG}" --format "{{.Size}}")
echo -e "${YELLOW}Image size: ${IMAGE_SIZE}${NC}"

# Test 3: Run container
echo -e "${BLUE}🚀 Test 3: Starting container...${NC}"
if docker run -d --name "${CONTAINER_NAME}" -p "${TEST_PORT}:8501" "${IMAGE_NAME}:${TAG}"; then
    echo -e "${GREEN}✅ Container started successfully${NC}"
else
    echo -e "${RED}❌ Container failed to start${NC}"
    exit 1
fi

# Test 4: Wait for application to be ready
echo -e "${BLUE}⏳ Test 4: Waiting for application to be ready...${NC}"
for i in {1..30}; do
    if curl -f "http://localhost:${TEST_PORT}/_stcore/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Application is ready${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}❌ Application failed to start within 30 seconds${NC}"
        docker logs "${CONTAINER_NAME}"
        exit 1
    fi
    sleep 1
done

# Test 5: Check application response
echo -e "${BLUE}🌐 Test 5: Testing application response...${NC}"
if curl -s "http://localhost:${TEST_PORT}" | grep -q "AI Notes Summarizer"; then
    echo -e "${GREEN}✅ Application responding correctly${NC}"
else
    echo -e "${RED}❌ Application not responding correctly${NC}"
    exit 1
fi

# Test 6: Check container logs for errors
echo -e "${BLUE}📝 Test 6: Checking container logs...${NC}"
if docker logs "${CONTAINER_NAME}" 2>&1 | grep -i error; then
    echo -e "${YELLOW}⚠️  Found errors in logs (see above)${NC}"
else
    echo -e "${GREEN}✅ No errors found in logs${NC}"
fi

# Test 7: Test Docker Compose
echo -e "${BLUE}🐙 Test 7: Testing Docker Compose...${NC}"
if docker-compose config > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Docker Compose configuration is valid${NC}"
else
    echo -e "${RED}❌ Docker Compose configuration is invalid${NC}"
    exit 1
fi

# Test 8: Security scan (if available)
echo -e "${BLUE}🔒 Test 8: Basic security check...${NC}"
if command -v docker &> /dev/null; then
    # Check if running as non-root
    USER_CHECK=$(docker exec "${CONTAINER_NAME}" whoami 2>/dev/null || echo "root")
    if [ "$USER_CHECK" != "root" ]; then
        echo -e "${GREEN}✅ Container running as non-root user: ${USER_CHECK}${NC}"
    else
        echo -e "${YELLOW}⚠️  Container running as root user${NC}"
    fi
fi

echo ""
echo -e "${GREEN}🎉 All tests passed successfully!${NC}"
echo ""
echo -e "${BLUE}📊 Test Summary:${NC}"
echo -e "${YELLOW}Image: ${IMAGE_NAME}:${TAG}${NC}"
echo -e "${YELLOW}Size: ${IMAGE_SIZE}${NC}"
echo -e "${YELLOW}Test URL: http://localhost:${TEST_PORT}${NC}"
echo ""
echo -e "${BLUE}🚀 Ready for deployment!${NC}"
