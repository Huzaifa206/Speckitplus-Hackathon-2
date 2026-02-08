# Data Model: Phase IV - Kubernetes Migration

**Date**: 2026-02-07
**Feature**: 004-k8s-migration

## Overview

This document describes the container and Kubernetes infrastructure entities for Phase IV. The application data model (Task, User, Conversation, Message) remains unchanged from Phase III.

## Infrastructure Entities

### Docker Image

Represents a containerized application with all dependencies bundled.

**Attributes**:
- `repository`: Registry path (e.g., `huzaifa206/todo-backend`)
- `tag`: Version identifier (e.g., `v1.0.0`, `latest`)
- `digest`: SHA256 hash of image contents
- `size`: Total size in MB
- `platform`: Target architecture (linux/amd64 or linux/arm64)
- `layers`: Ordered list of filesystem layers
- `created`: Timestamp of image creation
- `base_image`: Parent image (e.g., `python:3.9-alpine`)

**Lifecycle States**:
1. **Building**: Docker building layers from Dockerfile
2. **Built**: Image exists in local Docker cache
3. **Tagged**: Image tagged with repository and version
4. **Pushed**: Image uploaded to Docker Hub
5. **Available**: Image pullable from registry

**Relationships**:
- Referenced by Kubernetes Deployment
- Based on parent base image
- Stored in Docker Hub registry

**Validation Rules**:
- Tag must follow semantic versioning or `latest`
- Size should be < 500MB for optimization
- Must expose at least one port
- Must have ENTRYPOINT or CMD defined

---

### Kubernetes Deployment

Declarative specification of desired pod state.

**Attributes**:
- `name`: Deployment identifier (e.g., `backend-deployment`)
- `namespace`: Kubernetes namespace (default: `default`)
- `replicas`: Desired number of pod copies (default: 2)
- `selector`: Label selector for pods (e.g., `app: backend`)
- `template`: Pod template specification
  - `labels`: Key-value pairs for selection
  - `containers`: List of container specifications
    - `name`: Container name
    - `image`: Docker image reference
    - `ports`: Exposed ports
    - `env`: Environment variables
    - `envFrom`: Secret/ConfigMap references
    - `resources`: CPU/memory requests and limits
    - `livenessProbe`: Health check for restart
    - `readinessProbe`: Health check for traffic routing

**Lifecycle States**:
1. **Pending**: Deployment created, waiting for scheduler
2. **Progressing**: Pods being created
3. **Available**: All replicas running and ready
4. **Degraded**: Some replicas unavailable
5. **Failed**: Cannot create required replicas

**Relationships**:
- Creates and manages ReplicaSet
- ReplicaSet creates and manages Pods
- Pods pull Docker images
- Pods reference Secrets and ConfigMaps
- Selected by Service for traffic routing

**Validation Rules**:
- Replicas must be >= 1
- Selector must match template labels
- Image must be pullable
- Resource requests must be <= limits
- Probes must target valid endpoints

---

### Kubernetes Service

Network abstraction providing stable endpoint for pod access.

**Attributes**:
- `name`: Service identifier (e.g., `backend-service`)
- `namespace`: Kubernetes namespace (default: `default`)
- `type`: Service type (ClusterIP, NodePort, LoadBalancer)
  - ClusterIP: Internal cluster IP (default)
  - NodePort: External access via node IP:port
  - LoadBalancer: Cloud provider load balancer
- `selector`: Label selector to match pods
- `ports`: Port mappings
  - `port`: Service port (internal)
  - `targetPort`: Container port
  - `nodePort`: External port (NodePort only)
  - `protocol`: TCP or UDP
- `clusterIP`: Assigned internal IP address
- `endpoints`: List of pod IPs backing this service

**Lifecycle States**:
1. **Pending**: Service created, waiting for endpoints
2. **Active**: Service has endpoints and routing traffic
3. **Failed**: No matching pods found

**Relationships**:
- Routes traffic to pods matching selector
- DNS entry created: `<service-name>.<namespace>.svc.cluster.local`
- For NodePort: Exposed on all cluster nodes

**Validation Rules**:
- Selector must match at least one pod
- targetPort must match container port
- NodePort must be in range 30000-32767
- Type must be valid enum value

---

### Kubernetes Secret

Secure storage for sensitive configuration data.

**Attributes**:
- `name`: Secret identifier (e.g., `todo-secrets`)
- `namespace`: Kubernetes namespace (default: `default`)
- `type`: Secret type (Opaque, TLS, etc.)
- `data`: Key-value map of base64-encoded strings
  - `DATABASE_URL`: PostgreSQL connection string
  - `GEMINI_API_KEY`: Google Gemini API key
  - `JWT_SECRET_KEY`: JWT signing secret
- `stringData`: Alternative to `data`, not base64-encoded (not used in production)

**Lifecycle States**:
1. **Created**: Secret applied to cluster
2. **Mounted**: Referenced by running pods
3. **Updated**: Values changed (requires pod restart)
4. **Deleted**: Removed from cluster

**Relationships**:
- Referenced by Deployment via `envFrom` or `env`
- Mounted as environment variables in pods
- Can be mounted as files (not used in Phase IV)

**Validation Rules**:
- Keys must be valid environment variable names
- Values must be base64-encoded in `data` field
- Must not be committed to git with real values
- Should document encoding process for reproducibility

---

### Kubernetes Pod

Runtime instance of container(s).

**Attributes**:
- `name`: Generated name (e.g., `backend-deployment-abc123-xyz`)
- `namespace`: Kubernetes namespace
- `status`: Current state (Pending, Running, Succeeded, Failed, Unknown)
- `phase`: Lifecycle phase
- `conditions`: Detailed status information
- `containers`: List of containers in pod
- `ip`: Assigned pod IP address
- `nodeName`: Node where pod is running
- `restartCount`: Number of container restarts

**Lifecycle States**:
1. **Pending**: Waiting for scheduling or image pull
2. **Running**: At least one container is running
3. **Succeeded**: All containers terminated successfully
4. **Failed**: At least one container failed
5. **Unknown**: State cannot be determined
6. **CrashLoopBackOff**: Container repeatedly crashing

**Relationships**:
- Created and managed by ReplicaSet (via Deployment)
- Runs Docker container images
- Consumes Secrets and ConfigMaps
- Has IP address, routable within cluster
- Selected by Service for traffic

**Validation Rules**:
- Must have at least one container
- Container image must be pullable
- Resource requests must be satisfiable by cluster
- Probes must succeed for ready state

---

## Entity Relationships Diagram

```
Docker Hub Registry
    ↓ (stores)
Docker Images (backend:v1.0.0, frontend:v1.0.0)
    ↓ (referenced by)
Kubernetes Deployments (backend-deployment, frontend-deployment)
    ↓ (creates)
ReplicaSets
    ↓ (creates)
Pods (backend-pod-xxx, frontend-pod-xxx)
    ↑ (selected by)
Kubernetes Services (backend-service, frontend-service)
    ↓ (routes traffic to)
Pods
    ↓ (consume)
Kubernetes Secrets (todo-secrets)

External:
  Neon PostgreSQL ← (connected by) ← Backend Pods
```

---

## Configuration Flow

1. **Secret Creation**:
   - Engineer creates secret.yaml with base64-encoded values
   - `kubectl apply -f secret.yaml` creates Secret in cluster

2. **Image Preparation**:
   - Engineer builds Docker images locally
   - Images pushed to Docker Hub registry
   - Kubernetes can pull images via public URL

3. **Deployment Application**:
   - Engineer applies Deployment manifests
   - Deployment Controller creates ReplicaSets
   - ReplicaSets create Pods
   - Pods pull images from Docker Hub
   - Secrets mounted as environment variables in pods

4. **Service Exposure**:
   - Engineer applies Service manifests
   - Services create stable endpoints
   - DNS entries created for service discovery
   - Traffic routed to healthy pods via readiness probes

5. **Application Access**:
   - Users run `minikube service frontend-service`
   - Minikube creates tunnel or returns NodePort URL
   - Frontend served from nginx in pod
   - Frontend calls backend via internal service DNS

---

## State Management

### Stateless Components
- Frontend: Nginx serving static files (no state)
- Backend: FastAPI server (session state in JWT tokens)

### External State
- Database: Neon PostgreSQL (managed, external)
- Secrets: Kubernetes etcd (managed by Kubernetes)

### Ephemeral State
- Pod filesystem: Lost on pod restart
- Logs: Stored in pod, accessible via `kubectl logs`

**Implication**: Application is fully stateless, pods can be killed/restarted without data loss.

---

## Networking Model

### Internal Communication (Pod to Pod)
- Frontend pod → Backend Service (ClusterIP)
- DNS resolution: `backend-service` → Cluster IP → Pod IPs
- Protocol: HTTP over TCP
- Port: 8000

### External Communication (Pod to Internet)
- Backend pod → Neon PostgreSQL
- DNS resolution: Public DNS → Neon endpoint
- Protocol: PostgreSQL over TCP/SSL
- Authentication: Connection string with credentials

### External Access (User to App)
- User → Minikube tunnel/NodePort → Frontend Service → Frontend Pods
- Protocol: HTTP over TCP
- Port: 30080 (NodePort) → 3000 (container port)

---

## Security Model

### Secrets Management
- Sensitive values stored in Kubernetes Secrets
- Base64 encoded (not encrypted at rest in Minikube)
- Mounted as environment variables in pods
- Not logged or exposed in manifests

### Network Security
- Backend not externally accessible (ClusterIP only)
- Frontend only exposes HTTP (no direct backend access)
- Database connection over SSL (Neon requirement)

### Container Security
- Non-root users in containers (best practice)
- Minimal base images (alpine) reduce attack surface
- No secrets baked into images

---

## Operational Model

### Deployment
- Declarative: `kubectl apply -f phase-4/k8s/`
- Idempotent: Can be applied multiple times
- Version controlled: Manifests in git

### Scaling
- Horizontal: Increase replica count in Deployment
- Manual: `kubectl scale deployment <name> --replicas=N`
- Future: Horizontal Pod Autoscaler (HPA)

### Updates
- Rolling update: Change image tag in Deployment
- Kubernetes gradually replaces pods
- Zero downtime with readiness probes
- Rollback: `kubectl rollout undo deployment <name>`

### Monitoring
- Pod status: `kubectl get pods`
- Logs: `kubectl logs -f <pod-name>`
- Events: `kubectl get events`
- Resource usage: `kubectl top pods`

### Self-Healing
- Failed liveness probe → Pod restart
- CrashLoopBackOff → Exponential backoff restart
- Pod deleted → ReplicaSet creates replacement
- Node failure → Pods rescheduled to healthy nodes

---

## Data Persistence

Since this phase uses external Neon database, no Kubernetes-native persistence is required. All application data persists in Neon regardless of pod lifecycle.

**Future Consideration**: Phase V might add Kafka or other stateful components requiring PersistentVolumes.
