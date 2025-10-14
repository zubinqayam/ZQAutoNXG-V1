#!/bin/bash
# ZQAutoNXG - Deployment Script
# Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC
# Licensed under the Apache License, Version 2.0

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# ZQAutoNXG Configuration
APP_NAME="ZQAutoNXG"
APP_VERSION="6.0.0"
APP_BRAND="Powered by ZQ AI LOGIC™"
CONTAINER_NAME="zqautonxg"
CONTAINER_PORT="8000"
HOST_PORT="8000"

echo -e "${BLUE}"
echo "╔═════════════════════════════════════════════════════════════════╗"
echo "║                          ZQAutoNXG Deployment                          ║"
echo "║             Next-Generation eXtended Automation Platform             ║"
echo "║                      Powered by ZQ AI LOGIC™                       ║"
echo "║                                                                       ║"
echo "║  Version: ${APP_VERSION}        License: Apache 2.0                  ║"
echo "║  Copyright © 2025 Zubin Qayam — All Rights Reserved            ║"
echo "╚═════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to show usage
show_usage() {
    echo -e "${YELLOW}Usage: $0 [COMMAND]${NC}"
    echo ""
    echo "Commands:"
    echo "  dev       - Run in development mode (Python)"
    echo "  docker    - Build and run Docker container"
    echo "  build     - Build Docker image only"
    echo "  stop      - Stop running container"
    echo "  clean     - Remove container and image"
    echo "  health    - Check application health"
    echo "  logs      - Show application logs"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev      # Run in development mode"
    echo "  $0 docker   # Build and run container"
    echo "  $0 health   # Check if ZQAutoNXG is healthy"
}

# Function to check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed or not in PATH${NC}"
        exit 1
    fi
}

# Function to check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
        echo -e "${RED}❌ Python is not installed or not in PATH${NC}"
        exit 1
    fi
    
    PYTHON_CMD="python3"
    if ! command -v python3 &> /dev/null; then
        PYTHON_CMD="python"
    fi
    
    # Check Python version
    PYTHON_VERSION=$("$PYTHON_CMD" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if [[ "$(echo "$PYTHON_VERSION < 3.11" | bc -l)" -eq 1 ]]; then
        echo -e "${RED}❌ Python 3.11+ required. Current version: $PYTHON_VERSION${NC}"
        exit 1
    fi
}

# Function to run in development mode
run_dev() {
    echo -e "${BLUE}🚀 Starting ZQAutoNXG in development mode...${NC}"
    
    check_python
    
    # Install dependencies if needed
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
        "$PYTHON_CMD" -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
    
    # Install/upgrade dependencies
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Run ZQAutoNXG
    echo -e "${GREEN}✅ Starting ZQAutoNXG server...${NC}"
    echo -e "${BLUE}Visit: http://localhost:${HOST_PORT}${NC}"
    echo -e "${BLUE}API Documentation: http://localhost:${HOST_PORT}/docs${NC}"
    echo -e "${BLUE}Health Check: http://localhost:${HOST_PORT}/health${NC}"
    echo ""
    
    uvicorn zqautonxg.app:app --reload --host 0.0.0.0 --port "$HOST_PORT"
}

# Function to build Docker image
build_image() {
    echo -e "${BLUE}🐳 Building ZQAutoNXG Docker image...${NC}"
    
    check_docker
    
    docker build \
        --tag "$CONTAINER_NAME:latest" \
        --tag "$CONTAINER_NAME:gv2-novabase" \
        --label "org.opencontainers.image.title=ZQAutoNXG" \
        --label "org.opencontainers.image.description=Next-Generation eXtended Automation Platform - Powered by ZQ AI LOGIC™" \
        --label "org.opencontainers.image.vendor=ZQ AI LOGIC™" \
        --label "org.opencontainers.image.licenses=Apache-2.0" \
        --label "org.opencontainers.image.copyright=© 2025 Zubin Qayam — ZQAutoNXG" \
        .
        
    echo -e "${GREEN}✅ ZQAutoNXG Docker image built successfully${NC}"
}

# Function to run Docker container
run_docker() {
    echo -e "${BLUE}🚀 Deploying ZQAutoNXG with Docker...${NC}"
    
    check_docker
    
    # Stop existing container if running
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        echo -e "${YELLOW}🗑️ Stopping existing container...${NC}"
        docker stop "$CONTAINER_NAME"
        docker rm "$CONTAINER_NAME"
    fi
    
    # Build image if it doesn't exist
    if ! docker images -q "$CONTAINER_NAME:latest" | grep -q .; then
        build_image
    fi
    
    # Run container
    echo -e "${GREEN}✅ Starting ZQAutoNXG container...${NC}"
    docker run -d \
        --name "$CONTAINER_NAME" \
        --publish "$HOST_PORT:$CONTAINER_PORT" \
        --restart unless-stopped \
        --health-cmd="curl -f http://localhost:$CONTAINER_PORT/health || exit 1" \
        --health-interval=30s \
        --health-timeout=10s \
        --health-retries=3 \
        "$CONTAINER_NAME:latest"
    
    echo -e "${GREEN}✅ ZQAutoNXG deployed successfully${NC}"
    echo -e "${BLUE}Visit: http://localhost:${HOST_PORT}${NC}"
    echo -e "${BLUE}API Documentation: http://localhost:${HOST_PORT}/docs${NC}"
    echo -e "${BLUE}Health Check: http://localhost:${HOST_PORT}/health${NC}"
    
    # Wait for health check
    echo -e "${YELLOW}🔍 Waiting for ZQAutoNXG to be ready...${NC}"
    sleep 5
    check_health
}

# Function to stop container
stop_container() {
    echo -e "${YELLOW}🗑️ Stopping ZQAutoNXG container...${NC}"
    
    check_docker
    
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        docker stop "$CONTAINER_NAME"
        docker rm "$CONTAINER_NAME"
        echo -e "${GREEN}✅ ZQAutoNXG container stopped${NC}"
    else
        echo -e "${YELLOW}⚠️ No running ZQAutoNXG container found${NC}"
    fi
}

# Function to clean up
clean_up() {
    echo -e "${YELLOW}🧼 Cleaning up ZQAutoNXG resources...${NC}"
    
    check_docker
    
    # Stop container if running
    stop_container
    
    # Remove image if exists
    if docker images -q "$CONTAINER_NAME" | grep -q .; then
        echo -e "${YELLOW}🖼️ Removing ZQAutoNXG images...${NC}"
        docker rmi "$CONTAINER_NAME:latest" "$CONTAINER_NAME:gv2-novabase" 2>/dev/null || true
        echo -e "${GREEN}✅ ZQAutoNXG images removed${NC}"
    else
        echo -e "${YELLOW}⚠️ No ZQAutoNXG images found${NC}"
    fi
}

# Function to check application health
check_health() {
    echo -e "${BLUE}🔍 Checking ZQAutoNXG health...${NC}"
    
    if command -v curl &> /dev/null; then
        if curl -f -s "http://localhost:${HOST_PORT}/health" > /dev/null; then
            HEALTH_RESPONSE=$(curl -s "http://localhost:${HOST_PORT}/health")
            echo -e "${GREEN}✅ ZQAutoNXG is healthy!${NC}"
            echo -e "${BLUE}Response: $HEALTH_RESPONSE${NC}"
            
            # Get version info
            VERSION_RESPONSE=$(curl -s "http://localhost:${HOST_PORT}/version" 2>/dev/null || echo "")
            if [ -n "$VERSION_RESPONSE" ]; then
                echo -e "${BLUE}Version: $VERSION_RESPONSE${NC}"
            fi
        else
            echo -e "${RED}❌ ZQAutoNXG health check failed${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠️ curl not found, cannot perform health check${NC}"
    fi
}

# Function to show logs
show_logs() {
    echo -e "${BLUE}📜 Showing ZQAutoNXG logs...${NC}"
    
    check_docker
    
    if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
        docker logs -f "$CONTAINER_NAME"
    else
        echo -e "${RED}❌ No running ZQAutoNXG container found${NC}"
        exit 1
    fi
}

# Main script logic
case "${1:-help}" in
    "dev")
        run_dev
        ;;
    "docker")
        run_docker
        ;;
    "build")
        build_image
        ;;
    "stop")
        stop_container
        ;;
    "clean")
        clean_up
        ;;
    "health")
        check_health
        ;;
    "logs")
        show_logs
        ;;
    "help"|*)
        show_usage
        ;;
esac