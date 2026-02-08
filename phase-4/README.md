# Phase IV - Kubernetes Migration

**Status**: Active
**Date**: 2026-02-07
**Branch**: 004-k8s-migration

## Overview

Phase IV containerizes the Todo application using Docker and orchestrates it on local Kubernetes (Minikube). This demonstrates cloud-native architecture, containerization best practices, and orchestration skills.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Hub Registry                   │
│  - <username>/todo-backend:v1.0.0                       │
│  - <username>/todo-frontend:v1.0.0                      │
└─────────────────────────────────────────────────────────┘
                            ↓ (pulls images)
┌─────────────────────────────────────────────────────────┐
│                    Minikube Cluster                      │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │           Kubernetes Secrets                   │    │
│  │  - DATABASE_URL, GEMINI_API_KEY, JWT_SECRET   │    │
│  └────────────────────────────────────────────────┘    │
│                            ↓ (consumed by)              │
│  ┌─────────────────┐    ┌─────────────────┐           │
│  │ Frontend Pods   │    │ Backend Pods    │           │
│  │ (nginx:alpine)  │───→│ (FastAPI)       │───→ Neon  │
│  │ Replicas: 2     │    │ Replicas: 2     │     DB    │
│  └─────────────────┘    └─────────────────┘           │
│         ↑                        ↑                      │
│  frontend-service         backend-service              │
│  (NodePort:30080)         (ClusterIP:8000)             │
└─────────────────────────────────────────────────────────┘
         ↑
    User Browser
  (minikube-ip:30080)
```

## Components

### Backend Service
- **Technology**: FastAPI (Python 3.9)
- **Container**: Python alpine-based image
- **Port**: 8000
- **Service Type**: ClusterIP (internal only)
- **Replicas**: 2 pods for high availability
- **Health Check**: `/health` endpoint

### Frontend Service
- **Technology**: Next.js 14 with React
- **Container**: Multi-stage build (Node → nginx)
- **Port**: 3000 (NodePort: 30080)
- **Service Type**: NodePort (external access)
- **Replicas**: 2 pods for high availability
- **Health Check**: Root `/` endpoint

### Database
- **Technology**: Neon PostgreSQL (external)
- **Connection**: Backend pods connect via DATABASE_URL secret
- **Not containerized**: Using existing cloud-hosted database

## Directory Structure

```
phase-4/
├── backend/
│   ├── Dockerfile              # Backend container definition
│   ├── .dockerignore           # Exclude Python artifacts
│   ├── requirements.txt        # Python dependencies
│   └── [FastAPI application]   # Copied from phase-3
│
├── frontend/
│   ├── Dockerfile              # Multi-stage frontend build
│   ├── .dockerignore           # Exclude node artifacts
│   ├── nginx.conf              # SPA routing configuration
│   ├── next.config.js          # Next.js configuration
│   └── [Next.js application]   # Copied from phase-3
│
├── k8s/
│   ├── secret.yaml             # Kubernetes secrets
│   ├── backend-deployment.yaml # Backend pods
│   ├── backend-service.yaml    # Backend service
│   ├── frontend-deployment.yaml# Frontend pods
│   ├── frontend-service.yaml   # Frontend service
│   └── README.md               # Deployment guide
│
└── README.md                   # This file
```

## Prerequisites

- Docker Desktop installed and running
- Minikube installed
- kubectl CLI installed
- Docker Hub account created
- At least 4GB RAM available for Minikube

## Quick Start

1. **Start Minikube**:
   ```bash
   minikube start --cpus=2 --memory=4096
   ```

2. **Apply Kubernetes Manifests**:
   ```bash
   kubectl apply -f phase-4/k8s/secret.yaml
   kubectl apply -f phase-4/k8s/
   ```

3. **Access Application**:
   ```bash
   minikube service frontend-service
   ```

## Key Features

- **Self-Healing**: Pods automatically restart on failure
- **Scalable**: 2 replicas per service, can scale up/down
- **Secure**: Secrets managed via Kubernetes Secrets
- **Portable**: Runs on any Minikube/Kubernetes cluster
- **Optimized**: Multi-stage builds for minimal image sizes

## Success Metrics

- ✅ All pods reach Running status < 2 minutes
- ✅ Application accessible via Minikube
- ✅ Full CRUD functionality preserved
- ✅ Self-healing verified (pod restart < 30 seconds)
- ✅ Images optimized (backend < 300MB, frontend < 200MB)

## Next Steps

See `k8s/README.md` for detailed deployment instructions and troubleshooting.

For documentation, see `specs/004-k8s-migration/` directory:
- `spec.md` - Feature requirements
- `plan.md` - Implementation strategy
- `tasks.md` - Task breakdown
- `quickstart.md` - Deployment guide
