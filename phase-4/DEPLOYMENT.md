# Phase IV Deployment Guide

**Date**: 2026-02-07
**Status**: Ready for Deployment

## Overview

This guide walks you through deploying the Todo application to Kubernetes (Minikube).

## ✅ Completed Setup

- [x] Phase 4 directory structure created
- [x] Phase III code copied to phase-4/
- [x] Docker configurations created
- [x] Kubernetes manifests created
- [x] Health endpoints configured

## 📋 Prerequisites

Before deploying, ensure you have:

1. **Docker Desktop** installed and running
   ```bash
   docker --version
   ```

2. **Minikube** installed
   ```bash
   minikube version
   ```

3. **kubectl** installed
   ```bash
   kubectl version --client
   ```

4. **Docker Hub Account**
   - Sign up at https://hub.docker.com
   - Note your username (e.g., `huzaifa206`)

5. **System Resources**
   - At least 4GB RAM available
   - At least 20GB disk space

## 🚀 Deployment Steps

### Step 1: Build Docker Images

#### Backend Image

```bash
cd phase-4/backend

# Build the image
docker build --platform linux/amd64 -t huzaifa206/todo-backend:v1.0.0 .

# Test locally (optional)
docker run -p 8000:8000 \
  -e DATABASE_URL="your-neon-db-url" \
  -e GEMINI_API_KEY="your-api-key" \
  -e JWT_SECRET_KEY="your-jwt-secret" \
  huzaifa206/todo-backend:v1.0.0
```

#### Frontend Image

```bash
cd phase-4/frontend

# Build the image
docker build --platform linux/amd64 -t huzaifa206/todo-frontend:v1.0.0 .

# Test locally (optional)
docker run -p 3000:80 huzaifa206/todo-frontend:v1.0.0
```

### Step 2: Push Images to Docker Hub

```bash
# Login to Docker Hub
docker login

# Push backend
docker push huzaifa206/todo-backend:v1.0.0
docker tag huzaifa206/todo-backend:v1.0.0 huzaifa206/todo-backend:latest
docker push huzaifa206/todo-backend:latest

# Push frontend
docker push huzaifa206/todo-frontend:v1.0.0
docker tag huzaifa206/todo-frontend:v1.0.0 huzaifa206/todo-frontend:latest
docker push huzaifa206/todo-frontend:latest
```

### Step 3: Configure Secrets

**IMPORTANT**: Update `phase-4/k8s/secret.yaml` with your actual secrets before deploying!

```bash
# Encode your secrets
echo -n "postgresql://user:pass@host:5432/dbname?sslmode=require" | base64
echo -n "your-gemini-api-key" | base64
echo -n "your-jwt-secret-key-at-least-32-characters" | base64
```

Update the `data` section in `secret.yaml` with the encoded values.

### Step 4: Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=2 --memory=4096

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

Expected output: Cluster running, 1 node in Ready state

### Step 5: Deploy to Kubernetes

```bash
# Navigate to k8s directory
cd phase-4/k8s

# Apply secrets first
kubectl apply -f secret.yaml

# Apply all other manifests
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml

# Or apply all at once
kubectl apply -f .
```

### Step 6: Verify Deployment

```bash
# Watch pods starting (wait for all to show Running)
kubectl get pods -w

# Check pod status
kubectl get pods

# Expected output:
# NAME                                   READY   STATUS    RESTARTS   AGE
# backend-deployment-xxx-xxx             1/1     Running   0          1m
# backend-deployment-xxx-yyy             1/1     Running   0          1m
# frontend-deployment-xxx-xxx            1/1     Running   0          1m
# frontend-deployment-xxx-yyy            1/1     Running   0          1m

# Check services
kubectl get services

# Expected output:
# NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
# backend-service    ClusterIP   10.x.x.x        <none>        8000/TCP         1m
# frontend-service   NodePort    10.x.x.x        <none>        3000:30080/TCP   1m
```

### Step 7: Access the Application

```bash
# Get the frontend service URL
minikube service frontend-service --url

# Or open in browser automatically
minikube service frontend-service
```

The application should open in your browser at `http://<minikube-ip>:30080`

## 🧪 Testing

### Test 1: Basic Functionality

1. **Login**: Use your credentials to log in
2. **Create Task**: Add a new task via the UI
3. **List Tasks**: Verify tasks are displayed
4. **Update Task**: Edit a task
5. **Delete Task**: Remove a task
6. **Chatbot**: Test adding tasks via AI assistant

### Test 2: Self-Healing

```bash
# Get a backend pod name
kubectl get pods -l app=backend

# Delete one pod
kubectl delete pod <backend-pod-name>

# Watch it automatically recreate
kubectl get pods -w

# Should see new pod spinning up within 30 seconds
```

### Test 3: Scaling

```bash
# Scale backend to 3 replicas
kubectl scale deployment backend-deployment --replicas=3

# Verify scaling
kubectl get pods -l app=backend

# Should see 3 backend pods running

# Scale back to 2
kubectl scale deployment backend-deployment --replicas=2
```

### Test 4: Logs & Debugging

```bash
# View backend logs
kubectl logs -l app=backend

# View frontend logs
kubectl logs -l app=frontend

# Follow logs in real-time
kubectl logs -f <pod-name>

# Execute command in pod
kubectl exec -it <backend-pod-name> -- /bin/sh
```

## 📊 Monitoring

### Check Pod Status

```bash
# Detailed pod information
kubectl get pods -o wide

# Describe specific pod
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Resource usage (requires metrics-server)
kubectl top pods
kubectl top nodes
```

### Check Service Endpoints

```bash
# List services
kubectl get services

# Describe service
kubectl describe service backend-service

# Check endpoints
kubectl get endpoints
```

## 🔧 Troubleshooting

### Pods Not Starting

```bash
# Check pod events and status
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name>

# Common issues:
# - ImagePullBackOff: Wrong image name or not pushed to Docker Hub
# - CrashLoopBackOff: Application error, check logs
# - Pending: Insufficient resources, check kubectl top nodes
```

### Cannot Access Frontend

```bash
# Get Minikube IP
minikube ip

# Access via NodePort
curl http://$(minikube ip):30080

# Port forward as alternative
kubectl port-forward svc/frontend-service 3000:3000
```

### Database Connection Issues

```bash
# Verify secrets are loaded
kubectl exec <backend-pod-name> -- env | grep DATABASE_URL

# Test database connectivity
kubectl exec <backend-pod-name> -- sh -c "python -c 'import os; print(os.getenv(\"DATABASE_URL\"))'"
```

## 🧹 Cleanup

### Delete Deployment

```bash
# Delete all resources
kubectl delete -f phase-4/k8s/

# Verify deletion
kubectl get all
```

### Stop Minikube

```bash
# Stop cluster
minikube stop

# Delete cluster (full reset)
minikube delete
```

## 📈 Success Criteria

Verify these criteria are met:

- [ ] All pods reach Running status within 2 minutes
- [ ] Application accessible via `minikube service frontend-service`
- [ ] Login and authentication work
- [ ] All CRUD operations functional
- [ ] Chatbot works correctly
- [ ] Pod restart time < 30 seconds when manually deleted
- [ ] No secrets hardcoded in manifests or images

## 🎯 Next Steps

After successful deployment:

1. Document any issues encountered
2. Take screenshots of working application
3. Test with different user accounts
4. Prepare demo for judges
5. Review Phase IV success criteria from spec.md

## 📚 Additional Resources

- Kubernetes Manifests: `phase-4/k8s/`
- Architecture Diagram: `phase-4/README.md`
- Troubleshooting: `phase-4/k8s/README.md`
- Specifications: `specs/004-k8s-migration/`

For detailed troubleshooting, see `k8s/README.md`.
