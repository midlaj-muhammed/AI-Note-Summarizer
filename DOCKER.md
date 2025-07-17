# 🐳 Docker Deployment Guide

This guide covers Docker deployment options for the AI Notes Summarizer application.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available for Docker
- Internet connection for downloading AI models

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd ai-notes-summarizer

# Start the application
docker-compose up -d

# Access at http://localhost:8501
```

### Using Docker Scripts

```bash
# Build the image
./docker-build.sh

# Run the container
./docker-run.sh

# Test the deployment
./docker-test.sh
```

## 📁 Docker Files Overview

| File | Purpose |
|------|---------|
| `Dockerfile` | Standard multi-stage build |
| `Dockerfile.prod` | Production-optimized build |
| `docker-compose.yml` | Production deployment |
| `docker-compose.dev.yml` | Development environment |
| `docker-build.sh` | Build script |
| `docker-run.sh` | Run script |
| `docker-dev.sh` | Development script |
| `docker-test.sh` | Testing script |

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STREAMLIT_SERVER_PORT` | 8501 | Application port |
| `STREAMLIT_SERVER_ADDRESS` | 0.0.0.0 | Bind address |
| `TRANSFORMERS_CACHE` | /app/.cache/huggingface | Model cache directory |
| `MAX_FILE_SIZE_MB` | 10 | Maximum PDF file size |
| `TORCH_HOME` | /app/.cache/torch | PyTorch cache |

### Volume Mounts

| Volume | Purpose |
|--------|---------|
| `model_cache` | Persistent AI model storage |
| `logs` | Application logs |
| `uploads` | Temporary file storage |

## 🏗️ Build Options

### Standard Build
```bash
docker build -t ai-notes-summarizer .
```

### Production Build
```bash
docker build -f Dockerfile.prod -t ai-notes-summarizer:prod .
```

### Development Build
```bash
docker build --target dependencies -t ai-notes-summarizer:dev .
```

## 🚀 Deployment Options

### 1. Docker Compose (Production)

```yaml
# docker-compose.yml
version: '3.8'
services:
  ai-notes-summarizer:
    image: ai-notes-summarizer:latest
    ports:
      - "8501:8501"
    volumes:
      - model_cache:/app/.cache
      - logs:/app/logs
    restart: unless-stopped
```

### 2. Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml ai-notes-stack
```

### 3. Kubernetes

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-notes-summarizer
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ai-notes-summarizer
  template:
    metadata:
      labels:
        app: ai-notes-summarizer
    spec:
      containers:
      - name: ai-notes-summarizer
        image: ai-notes-summarizer:latest
        ports:
        - containerPort: 8501
        resources:
          limits:
            memory: "4Gi"
            cpu: "2"
          requests:
            memory: "2Gi"
            cpu: "1"
```

## 🔍 Monitoring and Logging

### Health Checks
```bash
# Check container health
docker ps --filter "name=ai-notes-summarizer"

# View health check logs
docker inspect ai-notes-summarizer | grep -A 10 Health
```

### Logs
```bash
# View application logs
docker-compose logs -f

# View specific service logs
docker logs -f ai-notes-summarizer
```

### Metrics
```bash
# Container stats
docker stats ai-notes-summarizer

# Resource usage
docker exec ai-notes-summarizer df -h
docker exec ai-notes-summarizer free -h
```

## 🛠️ Development

### Development Environment
```bash
# Start development environment with live reload
docker-compose -f docker-compose.dev.yml up

# Or use the script
./docker-dev.sh
```

### Debugging
```bash
# Access container shell
docker exec -it ai-notes-summarizer bash

# View application files
docker exec ai-notes-summarizer ls -la /app

# Check Python environment
docker exec ai-notes-summarizer pip list
```

## 🔒 Security

### Security Features
- Non-root user execution
- Minimal base image
- No unnecessary packages
- Health checks enabled
- Resource limits configured

### Security Scanning
```bash
# Scan for vulnerabilities (if you have docker scan)
docker scan ai-notes-summarizer:latest

# Check running processes
docker exec ai-notes-summarizer ps aux
```

## 🚨 Troubleshooting

### Common Issues

1. **Container won't start**
   ```bash
   docker logs ai-notes-summarizer
   ```

2. **Out of memory**
   ```bash
   # Increase Docker memory limit
   docker update --memory=4g ai-notes-summarizer
   ```

3. **Model download fails**
   ```bash
   # Check internet connectivity
   docker exec ai-notes-summarizer curl -I https://huggingface.co
   ```

4. **Permission issues**
   ```bash
   # Fix ownership
   docker exec -u root ai-notes-summarizer chown -R app:app /app
   ```

### Performance Optimization

1. **Use multi-stage builds** (already implemented)
2. **Enable BuildKit**:
   ```bash
   export DOCKER_BUILDKIT=1
   docker build .
   ```
3. **Use .dockerignore** (already included)
4. **Pin dependency versions** (see requirements.docker.txt)

## 📊 Resource Requirements

### Minimum Requirements
- CPU: 1 core
- RAM: 2GB
- Storage: 5GB

### Recommended Requirements
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB

### Production Requirements
- CPU: 4 cores
- RAM: 8GB
- Storage: 20GB
- Load balancer for multiple instances

## 🔄 Updates and Maintenance

### Updating the Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up --build -d

# Or use rolling update
docker-compose up -d --force-recreate
```

### Backup and Restore
```bash
# Backup volumes
docker run --rm -v ai-notes-model-cache:/data -v $(pwd):/backup alpine tar czf /backup/model-cache-backup.tar.gz -C /data .

# Restore volumes
docker run --rm -v ai-notes-model-cache:/data -v $(pwd):/backup alpine tar xzf /backup/model-cache-backup.tar.gz -C /data
```

## 📞 Support

For Docker-specific issues:
1. Check container logs: `docker logs ai-notes-summarizer`
2. Verify resource limits: `docker stats`
3. Test connectivity: `docker exec ai-notes-summarizer curl localhost:8501`
4. Review Docker documentation: https://docs.docker.com
