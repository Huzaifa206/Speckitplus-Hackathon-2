# Implementation Plan: Phase IV - Kubernetes Migration

**Branch**: `004-k8s-migration` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-k8s-migration/spec.md`

## Summary

Containerize the Phase III application (Next.js frontend + FastAPI backend) and orchestrate it on local Kubernetes (Minikube). Create production-ready Dockerfiles with multi-stage builds, push images to Docker Hub, and deploy using Kubernetes manifests with proper secret management, self-healing capabilities, and service discovery.

## Technical Context

**Language/Version**:
- Frontend: Node.js 18+, Next.js 14+
- Backend: Python 3.9+, FastAPI
- Container: Docker 24+, Kubernetes 1.28+

**Primary Dependencies**:
- Docker Desktop or equivalent container runtime
- Minikube for local Kubernetes cluster
- kubectl CLI for Kubernetes management
- Docker Hub account for image registry

**Storage**:
- Database: Neon PostgreSQL (cloud-hosted, not containerized)
- Secrets: Kubernetes Secrets (base64-encoded)
- Config: Kubernetes ConfigMaps for non-sensitive configuration

**Testing**:
- Container build testing: `docker build` validation
- Kubernetes deployment testing: `kubectl apply` + pod status checks
- Integration testing: End-to-end CRUD operations through deployed services
- Self-healing testing: Pod deletion and automatic restart verification

**Target Platform**: Linux containers (amd64 or arm64) running on Minikube (local Kubernetes)

**Project Type**: Web application with frontend and backend services

**Performance Goals**:
- Container startup time: < 30 seconds per pod
- Image pull time: < 2 minutes on first pull
- Application ready time: < 3 minutes from `kubectl apply` to fully functional
- Pod restart time: < 30 seconds for self-healing

**Constraints**:
- All Phase IV code must reside in `/phase-4` directory
- No modification to Phase III code
- No hardcoded secrets in images or manifests
- Images must be publicly accessible on Docker Hub
- Must work on local Minikube (no cloud provider required)
- Database remains external (Neon PostgreSQL)

**Scale/Scope**:
- 2 services to containerize (frontend, backend)
- 2 Docker images to build and publish
- 4-6 Kubernetes manifests to create (Deployments, Services, Secrets)
- Target: 2 replica pods per service for demonstration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase IV Compliance

✅ **Container-First Principle**: All artifacts will reside in `/phase-4` directory
✅ **Orchestration Principle**: Using Minikube and Kubernetes manifests
✅ **Self-Healing Principle**: Liveness and readiness probes will be configured
✅ **Isolation Principle**: Phase III code remains untouched in `/phase-3`
✅ **No Serverless**: Not using Vercel, Render, or cloud serverless platforms
✅ **Secret Management**: Using Kubernetes Secrets, no hardcoded credentials
✅ **Resource Limits**: Will specify resource requests/limits in manifests

### No Violations

All requirements align with constitution principles. No complexity violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/004-k8s-migration/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0: Technology research
├── data-model.md        # Phase 1: Container and K8s entity model
├── quickstart.md        # Phase 1: Deployment guide
├── contracts/           # Phase 1: Kubernetes manifest contracts
└── tasks.md             # Phase 2: Task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
phase-4/
├── backend/
│   ├── Dockerfile                    # Backend container definition
│   ├── .dockerignore                 # Exclude unnecessary files
│   ├── requirements.txt              # Python dependencies (copied from phase-3)
│   └── [source code copied from phase-3/backend/]
│
├── frontend/
│   ├── Dockerfile                    # Frontend multi-stage build
│   ├── .dockerignore                 # Exclude node_modules, .next
│   ├── package.json                  # Dependencies (copied from phase-3)
│   ├── next.config.js                # Next.js config
│   └── [source code copied from phase-3/frontend/]
│
├── k8s/
│   ├── namespace.yaml                # Optional: Dedicated namespace
│   ├── secret.yaml                   # Database credentials, API keys
│   ├── configmap.yaml                # Non-sensitive configuration
│   ├── backend-deployment.yaml       # Backend pod specification
│   ├── backend-service.yaml          # Backend service (ClusterIP)
│   ├── frontend-deployment.yaml      # Frontend pod specification
│   ├── frontend-service.yaml         # Frontend service (NodePort/LoadBalancer)
│   └── README.md                     # Deployment instructions
│
└── README.md                         # Phase 4 overview and setup guide
```

**Structure Decision**: Using web application structure (Option 2) with Phase IV isolation. The `/phase-4` directory contains copies of Phase III code plus new Docker and Kubernetes configurations. Original Phase III code remains unchanged in `/phase-3`.

## Complexity Tracking

No constitution violations. All complexity is justified by the phase requirements for containerization and orchestration.

---

## Phase 0: Research & Resolution

### Research Areas

1. **Docker Multi-Stage Builds for Next.js**
   - **Decision**: Use Node.js alpine base image for build stage, nginx alpine for serve stage
   - **Rationale**: Next.js static export can be served by lightweight nginx, reducing final image size significantly (from ~1GB to ~100MB)
   - **Alternatives considered**:
     - Single-stage Node image (rejected: too large, includes unnecessary build tools)
     - Standalone Next.js server (rejected: requires Node runtime, larger image)

2. **Kubernetes Secret Management**
   - **Decision**: Use Kubernetes Secrets with base64 encoding, reference as environment variables in pods
   - **Rationale**: Native Kubernetes secret management, integrates with RBAC, can be rotated without rebuilding images
   - **Alternatives considered**:
     - HashiCorp Vault (rejected: too complex for Phase IV, additional infrastructure)
     - Sealed Secrets (rejected: requires additional operator installation)

3. **Service Communication Pattern**
   - **Decision**: Backend uses ClusterIP service (internal only), Frontend uses NodePort service (external access via Minikube)
   - **Rationale**: Backend doesn't need external exposure, NodePort works well with Minikube for local development
   - **Alternatives considered**:
     - LoadBalancer for frontend (rejected: requires cloud provider or MetalLB setup)
     - Ingress controller (rejected: out of scope for Phase IV, adds complexity)

4. **Database Connection Strategy**
   - **Decision**: Backend pods connect directly to external Neon PostgreSQL via DATABASE_URL in Kubernetes Secret
   - **Rationale**: Neon is already hosted and working, no need to containerize database in Phase IV
   - **Alternatives considered**:
     - PostgreSQL in Kubernetes (rejected: adds state management complexity, out of scope)
     - Database proxy/pooler (rejected: unnecessary for local testing)

5. **Health Check Implementation**
   - **Decision**:
     - Backend: HTTP GET `/health` endpoint for liveness/readiness
     - Frontend: HTTP GET `/` (root) for liveness/readiness
   - **Rationale**: Simple HTTP checks are sufficient, already common practice in FastAPI and Next.js
   - **Alternatives considered**:
     - TCP socket checks (rejected: less informative than HTTP checks)
     - Exec-based checks (rejected: requires additional shell in container)

6. **Image Tagging Strategy**
   - **Decision**: Use semantic versioning with `v1.0.0` format, also maintain `latest` tag
   - **Rationale**: Allows rollback to specific versions, latest tag for convenience during development
   - **Alternatives considered**:
     - Git commit SHA tags (rejected: less human-readable)
     - Date-based tags (rejected: harder to track feature versions)

---

## Phase 1: Design & Contracts

### Data Model

**Entity: Docker Image**
- **Attributes**:
  - Repository name (e.g., `username/todo-backend`)
  - Tag (e.g., `v1.0.0`, `latest`)
  - Architecture (amd64 or arm64)
  - Size (target: < 500MB)
  - Base image (alpine variants for size optimization)
- **Lifecycle**: Built → Tagged → Pushed to registry → Pulled by Kubernetes
- **Relationships**: Referenced by Kubernetes Deployment manifest

**Entity: Kubernetes Deployment**
- **Attributes**:
  - Name (e.g., `backend-deployment`, `frontend-deployment`)
  - Replicas (2 for demonstration)
  - Container spec (image, ports, env vars, probes)
  - Resource limits (CPU: 500m, Memory: 512Mi)
  - Resource requests (CPU: 250m, Memory: 256Mi)
- **Lifecycle**: Applied → Managed by Deployment Controller → Creates ReplicaSets → Creates Pods
- **Relationships**: References Docker images, Secrets, ConfigMaps; creates Pods

**Entity: Kubernetes Service**
- **Attributes**:
  - Name (e.g., `backend-service`, `frontend-service`)
  - Type (ClusterIP for backend, NodePort for frontend)
  - Selector (matches Deployment labels)
  - Ports (container port → service port mapping)
- **Lifecycle**: Applied → Creates endpoint → Routes traffic to matching pods
- **Relationships**: Routes traffic to pods created by Deployment

**Entity: Kubernetes Secret**
- **Attributes**:
  - Name (e.g., `todo-secrets`)
  - Data (key-value pairs, base64-encoded)
  - Keys: DATABASE_URL, GEMINI_API_KEY, JWT_SECRET_KEY
- **Lifecycle**: Applied → Mounted as env vars or volumes in pods
- **Relationships**: Referenced by Deployments via envFrom or env

### API Contracts

Since this phase focuses on infrastructure, the API contracts are unchanged from Phase III. The existing REST API endpoints remain the same:

**Backend API** (FastAPI):
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register` - User registration
- `GET /api/users/{user_id}/tasks/` - List tasks
- `POST /api/users/{user_id}/tasks/` - Create task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete task
- `POST /api/chat/` - AI chatbot interaction
- `GET /health` - Health check endpoint (NEW for Kubernetes probes)

**Frontend** (Next.js):
- Serves static assets and React SPA
- Connects to backend via `NEXT_PUBLIC_API_URL` environment variable
- Internal Next.js API routes unchanged

### Container Contracts

**Backend Docker Image Contract**:
```yaml
Image: <dockerhub-username>/todo-backend:v1.0.0
Base: python:3.9-alpine
Exposed Ports: 8000
Entry Point: uvicorn main:app --host 0.0.0.0 --port 8000
Environment Variables Required:
  - DATABASE_URL (from Secret)
  - GEMINI_API_KEY (from Secret)
  - JWT_SECRET_KEY (from Secret)
  - JWT_ALGORITHM (from ConfigMap or default)
  - ACCESS_TOKEN_EXPIRE_MINUTES (from ConfigMap or default)
Health Checks:
  - /health endpoint returns 200 OK
Size Target: < 300MB
```

**Frontend Docker Image Contract**:
```yaml
Image: <dockerhub-username>/todo-frontend:v1.0.0
Base: nginx:alpine (serve stage)
Exposed Ports: 3000
Entry Point: nginx serving static Next.js build
Environment Variables Required:
  - NEXT_PUBLIC_API_URL (from ConfigMap, points to backend service)
Health Checks:
  - Root / returns 200 OK
Size Target: < 200MB
```

### Kubernetes Manifest Contracts

**Backend Deployment Contract**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    spec:
      containers:
      - name: backend
        image: <dockerhub-username>/todo-backend:v1.0.0
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: todo-secrets
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**Backend Service Contract**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
```

**Frontend Deployment Contract**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    spec:
      containers:
      - name: frontend
        image: <dockerhub-username>/todo-frontend:v1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://backend-service:8000"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "250m"
```

**Frontend Service Contract**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - protocol: TCP
    port: 3000
    targetPort: 3000
    nodePort: 30080  # Accessible at minikube-ip:30080
```

**Secrets Contract**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
type: Opaque
data:
  DATABASE_URL: <base64-encoded-value>
  GEMINI_API_KEY: <base64-encoded-value>
  JWT_SECRET_KEY: <base64-encoded-value>
```

### Quickstart Guide

See `quickstart.md` for step-by-step deployment instructions.

---

## Phase 2: Tasks & Verification

Tasks will be generated by `/sp.tasks` command. This section intentionally left for task breakdown.

---

## Architecture Decisions

### ADR-001: Use Multi-Stage Docker Build for Frontend

**Context**: Frontend Docker image size optimization

**Decision**: Use multi-stage build with separate build and serve stages

**Rationale**:
- Build stage: Node.js image with all dev dependencies (~1GB)
- Serve stage: nginx:alpine serving static build (~100MB)
- Reduces final image size by 90%
- Faster deployment and reduced registry storage costs

**Consequences**:
- Requires Next.js static export configuration
- Build time slightly longer (multi-stage overhead)
- Nginx configuration needed for SPA routing

### ADR-002: Backend as ClusterIP, Frontend as NodePort

**Context**: Service exposure strategy for Minikube

**Decision**:
- Backend: ClusterIP (internal-only)
- Frontend: NodePort (external access)

**Rationale**:
- Backend doesn't need external exposure (only frontend calls it)
- ClusterIP provides internal service discovery
- NodePort works well with Minikube for local testing
- Simpler than Ingress controller setup

**Consequences**:
- Frontend accesses backend via internal DNS (backend-service:8000)
- Users access frontend via minikube service command or NodePort
- Cannot directly access backend API from host (would need port-forward)

### ADR-003: External Database (Neon) vs Containerized PostgreSQL

**Context**: Database deployment strategy

**Decision**: Keep using external Neon PostgreSQL, do not containerize database

**Rationale**:
- Neon is already configured and working
- Database containerization adds state management complexity
- Phase IV focuses on application containerization, not data layer
- Reduces local resource requirements
- Demonstrates hybrid cloud-local architecture

**Consequences**:
- Backend pods must have internet access to reach Neon
- Database credentials stored in Kubernetes Secrets
- Cannot fully demonstrate end-to-end Kubernetes data management
- Future Phase V can add Kafka and more sophisticated patterns

### ADR-004: Raw Kubernetes Manifests vs Helm Charts

**Context**: Kubernetes deployment packaging

**Decision**: Use raw Kubernetes YAML manifests, not Helm charts

**Rationale**:
- Raw manifests are more transparent and educational
- No additional Helm installation required
- Simpler for judges to review and understand
- Sufficient for Phase IV scope (single environment)

**Consequences**:
- Manual templating for environment-specific values
- No built-in release management
- Easier to learn and debug for beginners
- Future phases can adopt Helm if needed

---

## Implementation Approach

### Step 1: Directory Setup
1. Create `/phase-4` directory structure
2. Copy Phase III code to phase-4/backend and phase-4/frontend
3. Create k8s/ directory for manifests

### Step 2: Docker Backend
1. Verify/create backend Dockerfile (may exist from Phase III)
2. Add .dockerignore for Python artifacts
3. Ensure requirements.txt is complete
4. Add /health endpoint to FastAPI if missing
5. Build and test locally: `docker build -t todo-backend:local .`
6. Run and verify: `docker run -p 8000:8000 todo-backend:local`

### Step 3: Docker Frontend
1. Create frontend Dockerfile with multi-stage build:
   - Stage 1: Install dependencies and build Next.js
   - Stage 2: Copy build output to nginx:alpine
2. Configure nginx for SPA routing
3. Add .dockerignore for node_modules, .next
4. Update next.config.js for static export if needed
5. Build and test: `docker build -t todo-frontend:local .`
6. Run and verify: `docker run -p 3000:80 todo-frontend:local`

### Step 4: Docker Hub Publishing
1. Tag images with Docker Hub username:
   - `docker tag todo-backend:local <username>/todo-backend:v1.0.0`
   - `docker tag todo-frontend:local <username>/todo-frontend:v1.0.0`
2. Login to Docker Hub: `docker login`
3. Push images:
   - `docker push <username>/todo-backend:v1.0.0`
   - `docker push <username>/todo-frontend:v1.0.0`
4. Create `latest` tags and push

### Step 5: Kubernetes Manifests
1. Create secret.yaml:
   - Base64 encode DATABASE_URL, GEMINI_API_KEY, JWT_SECRET_KEY
   - Use `echo -n "value" | base64` for encoding
2. Create backend-deployment.yaml:
   - 2 replicas for scaling demonstration
   - Reference todo-secrets for env vars
   - Add liveness/readiness probes
   - Set resource requests/limits
3. Create backend-service.yaml:
   - Type: ClusterIP
   - Port: 8000
4. Create frontend-deployment.yaml:
   - 2 replicas
   - Set NEXT_PUBLIC_API_URL to backend-service
   - Add liveness/readiness probes
   - Set resource requests/limits
5. Create frontend-service.yaml:
   - Type: NodePort
   - Port: 3000, NodePort: 30080

### Step 6: Minikube Deployment
1. Start Minikube: `minikube start --cpus=2 --memory=4096`
2. Verify cluster: `kubectl cluster-info`
3. Apply secrets first: `kubectl apply -f phase-4/k8s/secret.yaml`
4. Apply all manifests: `kubectl apply -f phase-4/k8s/`
5. Check pod status: `kubectl get pods`
6. Check services: `kubectl get services`
7. Access application: `minikube service frontend-service`

### Step 7: Testing & Verification
1. Verify all pods are Running
2. Check logs: `kubectl logs -l app=backend`
3. Test CRUD operations through UI
4. Test self-healing: `kubectl delete pod <backend-pod-name>`
5. Verify pod auto-recreates
6. Test scaling: `kubectl scale deployment backend-deployment --replicas=3`

---

## Testing Strategy

### Container Testing
- Build validation: Ensure Dockerfiles build without errors
- Size validation: Verify images are under size targets
- Runtime validation: Run containers locally and test basic functionality
- Security scan: Run `docker scan` to check for vulnerabilities

### Kubernetes Testing
- Manifest validation: `kubectl apply --dry-run=client`
- Deployment validation: All pods reach Running status
- Service validation: Services have endpoints
- Secret validation: Pods can read secret values
- Probe validation: Liveness/readiness checks pass
- Self-healing validation: Pods restart automatically on failure
- Integration testing: Full CRUD workflow through deployed application

### Acceptance Testing
- Deploy from scratch following quickstart.md
- Verify all success criteria from spec.md
- Test on clean Minikube cluster
- Validate with person unfamiliar with project

---

## Risk Assessment

### High Risk
- **Docker image build failures**: Dependency resolution issues, platform incompatibility
  - *Mitigation*: Test locally first, use proven base images, pin dependency versions

- **Kubernetes networking issues**: Pods can't communicate, services not discoverable
  - *Mitigation*: Use standard Kubernetes DNS, test with kubectl exec, verify service selectors

- **Secret management errors**: Misconfigured secrets, encoding issues
  - *Mitigation*: Validate base64 encoding, test secret values, use kubectl describe to debug

### Medium Risk
- **Resource constraints**: Minikube runs out of memory/CPU
  - *Mitigation*: Set appropriate resource limits, recommend minimum 4GB RAM, monitor with `kubectl top`

- **Image pull failures**: Rate limits, network issues, wrong image names
  - *Mitigation*: Use imagePullPolicy: IfNotPresent, verify image names, test pulls manually

### Low Risk
- **Image size exceeds targets**: Larger than expected, slow pulls
  - *Mitigation*: Use multi-stage builds, alpine base images, .dockerignore properly

---

## Rollback Strategy

1. If Kubernetes deployment fails: `kubectl delete -f phase-4/k8s/`
2. If images have issues: Rebuild and push new version, update manifests
3. Phase III remains untouched and can be run locally as fallback
4. Minikube cluster can be reset: `minikube delete && minikube start`

---

## Future Considerations (Phase V)

- Add Kafka for messaging
- Implement Dapr for service orchestration
- Deploy to DigitalOcean DOKS (managed Kubernetes)
- Add Ingress controller for proper routing
- Implement horizontal pod autoscaling
- Add monitoring (Prometheus/Grafana)
- Persistent volumes for stateful components

---

## Post-Design Constitution Check

✅ All Phase IV principles maintained:
- Container-First: All code in /phase-4 ✅
- Orchestration: Using Kubernetes manifests ✅
- Self-Healing: Probes configured ✅
- No Serverless: Using Minikube ✅
- Secret Management: Kubernetes Secrets ✅

No violations. Ready for `/sp.tasks`.
