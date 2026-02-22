#!/bin/bash
# Deployment script for Sentiport

set -e

echo "================================"
echo "Sentiport Deployment Script"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${YELLOW}[1/6]${NC} Checking prerequisites..."
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed!${NC}"
    exit 1
fi
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker and Docker Compose found${NC}"
echo ""

# Build images
echo -e "${YELLOW}[2/6]${NC} Building Docker images..."
docker-compose build
echo -e "${GREEN}✓ Docker images built${NC}"
echo ""

# Stop existing containers
echo -e "${YELLOW}[3/6]${NC} Stopping existing containers..."
docker-compose down 2>/dev/null || true
echo -e "${GREEN}✓ Containers stopped${NC}"
echo ""

# Start services
echo -e "${YELLOW}[4/6]${NC} Starting services..."
docker-compose up -d
echo -e "${GREEN}✓ Services started${NC}"
echo ""

# Wait for services to be healthy
echo -e "${YELLOW}[5/6]${NC} Waiting for services to be healthy..."
max_attempts=30
attempt=1

while [ $attempt -le $max_attempts ]; do
    if curl -f http://localhost:5000/api/health &> /dev/null; then
        echo -e "${GREEN}✓ API is healthy${NC}"
        break
    fi
    echo "Attempt $attempt/$max_attempts: Waiting for API..."
    sleep 2
    ((attempt++))
done

if [ $attempt -gt $max_attempts ]; then
    echo -e "${RED}API health check failed after $max_attempts attempts${NC}"
    docker-compose logs api
    exit 1
fi
echo ""

# Display deployment summary
echo -e "${YELLOW}[6/6]${NC} Deployment Summary"
echo -e "${GREEN}================================${NC}"
echo -e "API Server:      ${GREEN}http://localhost:5000${NC}"
echo -e "Frontend:        ${GREEN}http://localhost${NC}"
echo -e "API Health:      ${GREEN}http://localhost:5000/api/health${NC}"
echo ""
echo -e "To view logs:    ${YELLOW}docker-compose logs -f${NC}"
echo -e "To stop:         ${YELLOW}docker-compose down${NC}"
echo ""
echo -e "${GREEN}✓ Deployment complete!${NC}"
