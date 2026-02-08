# Kubernetes Deployment Guide

**Phase**: IV - Kubernetes Migration
**Date**: 2026-02-07

## Quick Deployment

### Prerequisites

- [ ] Docker Desktop installed and running
- [ ] Minikube installed (`minikube version`)
- [ ] kubectl installed (`kubectl version`)
- [ ] Docker Hub account created
- [ ] At least 4GB RAM available

### Step 1: Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=2 --memory=4096

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

Expected: Cluster running, 1 node in Ready state

### Step 2: Create Secrets

**Important**: Never commit `secret.yaml` with real values!

```bash
# Encode your secrets (replace with your actual values)
echo -n "postgresql://user:pass@host/db" | base64
echo -n "your-gemini-api-key" | base64
echo -n "your-jwt-secret-key" | base64
```

Update `secret.yaml` with the encoded values, then apply:

```bash
kubectl apply -f secret.yaml
```

Verify secrets created:
```bash
kubectl get secrets
kubectl describe secret todo-secrets
```

### Step 3: Deploy Application

```bash
# Apply all manifests
kubectl apply -f .

# Watch pods starting
kubectl get pods -w
```

Wait for all pods to show `Running` status (1-2 minutes).

### Step 4: Access Application

```bash
# Get frontend URL
minikube service frontend-service --url

# Or open in browser automatically
minikube service frontend-service
```

The application should open in your browser!

## Kubernetes Resources

### Deployments

**Backend Deployment** (`backend-deployment.yaml`):
- 2 replica pods
- Python 3.9 alpine base
- Port 8000
- Health checks on `/health`
- Resource limits: 512Mi memory, 500m CPU

**Frontend Deployment** (`frontend-deployment.yaml`):
- 2 replica pods
- nginx alpine serving static Next.js
- Port 3000
- Health checks on `/`
- Resource limits: 256Mi memory, 250m CPU

### Services

**Backend Service** (`backend-service.yaml`):
- Type: ClusterIP (internal only)
- Port: 8000
- DNS: `backend-service.default.svc.cluster.local`

**Frontend Service** (`frontend-service.yaml`):
- Type: NodePort
- Port: 3000
- NodePort: 30080
- External access via Minikube

### Secrets

**todo-secrets** (`secret.yaml`):
- DATABASE_URL: Neon PostgreSQL connection string
- GEMINI_API_KEY: Google Gemini API key
- JWT_SECRET_KEY: JWT signing secret

## Useful Commands

### Check Status

```bash
# View all resources
kubectl get all

# Check pod status
kubectl get pods
kubectl get pods -o wide

# Check services
kubectl get services
kubectl get endpoints

# Check secrets
kubectl get secrets
```

### View Logs

```bash
# View logs for specific pod
kubectl logs <pod-name>

# Follow logs
kubectl logs -f <pod-name>

# View logs for all backend pods
kubectl logs -l app=backend

# View logs for all frontend pods
kubectl logs -l app=frontend
```

### Debugging

```bash
# Describe resource for details
kubectl describe pod <pod-name>
kubectl describe service backend-service
kubectl describe deployment backend-deployment

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/sh

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check resource usage
kubectl top pods
kubectl top nodes
```

### Scaling

```bash
# Scale deployment
kubectl scale deployment backend-deployment --replicas=3

# Verify scaling
kubectl get pods -l app=backend

# Scale back
kubectl scale deployment backend-deployment --replicas=2
```

### Updates

```bash
# Update image version
kubectl set image deployment/backend-deployment backend=<username>/todo-backend:v1.0.1

# Check rollout status
kubectl rollout status deployment/backend-deployment

# Rollback if needed
kubectl rollout undo deployment/backend-deployment
```

### Cleanup

```bash
# Delete all resources
kubectl delete -f .

# Or delete specific resources
kubectl delete deployment backend-deployment frontend-deployment
kubectl delete service backend-service frontend-service
kubectl delete secret todo-secrets

# Stop Minikube
minikube stop

# Delete Minikube cluster (full reset)
minikube delete
```

## Troubleshooting

### Pods Not Starting

**Symptom**: Pods stuck in `Pending`, `ImagePullBackOff`, or `CrashLoopBackOff`

**Check**:
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Common Causes**:
- Image pull failure: Verify image name and Docker Hub accessibility
- Resource constraints: Check `kubectl top nodes`
- Missing secrets: Verify `kubectl get secrets`
- Crash on startup: Check logs for application errors

### Cannot Access Frontend

**Symptom**: `minikube service` doesn't work or shows error

**Solutions**:
```bash
# Get service URL manually
minikube service frontend-service --url

# Access via NodePort
curl http://$(minikube ip):30080

# Port forward as alternative
kubectl port-forward svc/frontend-service 3000:3000
```

### Backend Cannot Connect to Database

**Symptom**: Backend pods crash or logs show database errors

**Check**:
```bash
# Verify DATABASE_URL is set
kubectl exec <backend-pod> -- env | grep DATABASE_URL

# Test database connectivity
kubectl exec <backend-pod> -- curl -v <database-host>
```

**Solutions**:
- Verify DATABASE_URL is correctly encoded in secret
- Check internet connectivity from pods
- Verify Neon database is accessible

### Secrets Not Loading

**Symptom**: Pods can't read environment variables

**Check**:
```bash
# Verify secret exists
kubectl get secret todo-secrets

# Check secret data
kubectl describe secret todo-secrets

# Check pod environment
kubectl exec <pod-name> -- env
```

**Solutions**:
- Verify secret name matches in Deployment
- Check `envFrom` or `env` configuration
- Restart pods: `kubectl rollout restart deployment <name>`

## Health Checks

Both services have health probes configured:

### Backend Health
```bash
# Check health endpoint
kubectl exec <backend-pod> -- curl http://localhost:8000/health
```

Expected: `{"status": "healthy"}`

### Frontend Health
```bash
# Check frontend is serving
kubectl exec <frontend-pod> -- curl http://localhost:3000/
```

Expected: HTML response

## Performance Monitoring

```bash
# Watch pod resource usage
kubectl top pods --watch

# Check node resources
kubectl top nodes

# View pod metrics
kubectl describe pod <pod-name> | grep -A 5 "Requests\|Limits"
```

## Security Notes

- **Never commit secret.yaml with real values**
- Secrets are base64-encoded, not encrypted
- For production, use external secret management (Vault, AWS Secrets Manager)
- Review pod security contexts before production deployment

## Next Steps

After successful deployment:
1. Test all application functionality
2. Verify self-healing (delete pods)
3. Test scaling (increase replicas)
4. Document any issues or improvements
5. Prepare demo for judges

For detailed specifications, see `../specs/004-k8s-migration/` directory.
