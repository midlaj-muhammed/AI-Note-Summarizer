#!/bin/bash

# AI Notes Summarizer - Docker Development Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛠️  Starting AI Notes Summarizer in Development Mode${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed. Please install it and try again.${NC}"
    exit 1
fi

# Create necessary directories
mkdir -p logs uploads

# Start development environment
echo -e "${BLUE}🐳 Starting development environment...${NC}"
docker-compose -f docker-compose.dev.yml up --build

echo -e "${GREEN}✅ Development environment stopped.${NC}"
