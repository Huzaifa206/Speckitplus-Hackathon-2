# Quickstart: Phase IV - Kubernetes Deployment

**Feature**: 004-k8s-migration
**Date**: 2026-02-07

## Prerequisites

Before starting, ensure you have:

- [ ] **Docker Desktop** installed and running
- [ ] **Minikube** installed (`brew install minikube` or download from minikube.sigs.k8s.io)
- [ ] **kubectl** installed (usually comes with Docker Desktop)
- [ ] **Docker Hub account** created (hub.docker.com)
- [ ] **At least 4GB RAM** available for Minikube
- [ ] **Internet connection** for pulling images and accessing Neon database

## Quick Setup (10 Minutes)

### Step 1: Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=2 --memory=4096

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

Expected output: Cluster running, 1 node in Ready state

---

### Step 2: Prepare Secrets

Create a file `phase-4/k8s/secret.yaml` with your encoded secrets:

```bash
# Encode your secrets (do this locally, don't commit)
echo -n "postgresql://user:pass@host/db" | base64
echo -n "your-gemini-api-key" | base64
echo -n "your-jwt-secret" | base64
```

Update `phase-4/k8s/secret.yaml` with the encoded values.

---

### Step 3: Deploy to Kubernetes

```bash
# Navigate to repository root
cd E:\ai code\python\Speckitplus-Hackathon-II

# Apply secrets first
kubectl apply -f phase-4/k8s/secret.yaml

# Apply all other manifests
kubectl apply -f phase-4/k8s/

# Check deployment status
kubectl get pods
kubectl get services
```

Wait for all pods to show `Running` status (1-2 minutes).

---

### Step 4: Access the Application

```bash
# Get the frontend service URL
minikube service frontend-service --url

# Or open in browser automatically
minikube service frontend-service
```

The application should open in your browser!

---

### Step 5: Verify Functionality

1. **Test Login**: Log in with your credentials
2. **Test CRUD**: Create, view, update, delete tasks
3. **Test Chatbot**: Add tasks via AI assistant
4. **Test Self-Healing**: Delete a pod and watch it recreate
   ```bash
   kubectl delete pod <backend-pod-name>
   kubectl get pods -w
   ```

---

## Building Images (Optional)

If you need to rebuild images (e.g., code changes):

### Backend Image

```bash
cd phase-4/backend

# Build image
docker build -t <dockerhub-username>/todo-backend:v1.0.0 .

# Test locally
docker run -p 8000:8000 \
  -e DATABASE_URL="your-db-url" \
  -e GEMINI_API_KEY="your-key" \
  -e JWT_SECRET_KEY="your-secret" \
  <dockerhub-username>/todo-backend:v1.0.0

# Push to Docker Hub
docker login
docker push <dockerhub-username>/todo-backend:v1.0.0
docker tag <dockerhub-username>/todo-backend:v1.0.0 <dockerhub-username>/todo-backend:latest
docker push <dockerhub-username>/todo-backend:latest
```

### Frontend Image

```bash
cd phase-4/frontend

# Build image
docker build -t <dockerhub-username>/todo-frontend:v1.0.0 .

# Test locally
docker run -p 3000:80 <dockerhub-username>/todo-frontend:v1.0.0

# Push to Docker Hub
docker login
docker push <dockerhub-username>/todo-frontend:v1.0.0
docker tag <dockerhub-username>/todo-frontend:v1.0.0 <dockerhub-username>/todo-frontend:latest
docker push <dockerhub-username>/todo-frontend:latest
```

After pushing new images, update the image references in Deployment manifests and reapply:

```bash
kubectl apply -f phase-4/k8s/backend-deployment.yaml
kubectl apply -f phase-4/k8s/frontend-deployment.yaml
```

---

## Useful Commands

### Check Status

```bash
# View all resources
kubectl get all

# Check pod status with details
kubectl get pods -o wide

# Check pod logs
kubectl logs -f <pod-name>

# Check logs for all backend pods
kubectl logs -l app=backend

# Describe a resource for details
kubectl describe pod <pod-name>
kubectl describe service backend-service
kubectl describe secret todo-secrets
```

### Debugging

```bash
# Execute command in pod
kubectl exec -it <pod-name> -- /bin/sh

# Check pod events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check resource usage
kubectl top pods
kubectl top nodes

# Port forward to backend (if needed)
kubectl port-forward svc/backend-service 8000:8000
```

### Scaling

```bash
# Scale deployment
kubectl scale deployment backend-deployment --replicas=3

# Verify scaling
kubectl get pods -l app=backend
```

### Cleanup

```bash
# Delete all resources
kubectl delete -f phase-4/k8s/

# Or delete specific resources
kubectl delete deployment backend-deployment
kubectl delete service backend-service
kubectl delete secret todo-secrets

# Stop Minikube
minikube stop

# Delete Minikube cluster (full reset)
minikube delete
```

---

## Troubleshooting

### Pods Not Starting

**Symptom**: Pods stuck in `Pending`, `ImagePullBackOff`, or `CrashLoopBackOff`

**Solutions**:
1. Check pod events: `kubectl describe pod <pod-name>`
2. Check logs: `kubectl logs <pod-name>`
3. Verify image name is correct in Deployment
4. Verify secrets are created: `kubectl get secrets`
5. Check resource availability: `kubectl top nodes`

### Cannot Access Frontend

**Symptom**: `minikube service` doesn't open browser or shows error

**Solutions**:
1. Check service exists: `kubectl get svc frontend-service`
2. Check pods are ready: `kubectl get pods -l app=frontend`
3. Get service URL manually: `minikube service frontend-service --url`
4. Try accessing via NodePort: `http://$(minikube ip):30080`

### Backend Cannot Connect to Database

**Symptom**: Backend pods crash or logs show database connection errors

**Solutions**:
1. Verify DATABASE_URL is correct in secret
2. Check base64 encoding is valid
3. Test database connection from pod:
   ```bash
   kubectl exec -it <backend-pod> -- sh
   env | grep DATABASE_URL
   ```
4. Ensure pods have internet access (Minikube usually does by default)

### Secrets Not Loading

**Symptom**: Pods can't read environment variables from secrets

**Solutions**:
1. Verify secret exists: `kubectl get secret todo-secrets`
2. Check secret data: `kubectl describe secret todo-secrets`
3. Verify Deployment references correct secret name
4. Check envFrom or env configuration in Deployment
5. Restart pods to pick up secret changes: `kubectl rollout restart deployment <name>`

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Hub Registry                   │
│  - huzaifa206/todo-backend:v1.0.0                       │
│  - huzaifa206/todo-frontend:v1.0.0                      │
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

---

## Next Steps

After successful deployment:

1. **Test all functionality**: CRUD operations, chatbot, authentication
2. **Test self-healing**: Delete pods and verify auto-recreation
3. **Test scaling**: Increase replica count
4. **Document findings**: Screenshot working application
5. **Prepare demo**: Practice showing the deployment process

Ready to proceed with `/sp.tasks` for detailed task breakdown!
