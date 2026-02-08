# Research: Phase IV - Kubernetes Migration

**Date**: 2026-02-07
**Feature**: 004-k8s-migration

## Research Findings

### 1. Docker Multi-Stage Builds for Next.js

**Investigation**: Best practices for containerizing Next.js applications

**Findings**:
- Next.js can be deployed as standalone server (Node.js runtime) or static export (nginx/Apache)
- Multi-stage builds can reduce image size from 1GB+ to ~100MB
- Alpine base images provide minimal footprint while maintaining functionality
- Static export requires proper nginx configuration for client-side routing

**Decision**: Multi-stage build with Node.js for build, nginx for serving

**Rationale**:
- 90% reduction in image size (faster pulls, less storage)
- nginx is production-grade static file server
- Reduces attack surface (no Node.js runtime in production)
- Lower resource requirements (memory/CPU)

**Implementation Notes**:
- Stage 1: `node:18-alpine` for `npm install` and `npm run build`
- Stage 2: `nginx:alpine` serving `/out` or `/build` directory
- nginx.conf must handle SPA routing (all routes → index.html)
- Environment variables must be injected at build time for Next.js

---

### 2. Kubernetes Secret Management

**Investigation**: Options for managing sensitive configuration in Kubernetes

**Findings**:
- Kubernetes Secrets: Native, base64-encoded, RBAC-integrated
- Sealed Secrets: Encrypted at rest, requires CRD and controller
- External Secrets Operator: Syncs from external vaults (AWS Secrets Manager, etc.)
- HashiCorp Vault: Full-featured secret management, requires separate infrastructure

**Decision**: Native Kubernetes Secrets with base64 encoding

**Rationale**:
- No additional tooling or infrastructure required
- Works out-of-the-box with Minikube
- Sufficient security for Phase IV local testing
- Simple to understand and debug
- Integrates with kubectl and standard workflows

**Implementation Notes**:
- Base64 encode secrets: `echo -n "secret-value" | base64`
- Reference in pods via `envFrom` or individual `env` entries
- Never commit secret.yaml with real values (use .gitignore)
- Document secret creation process for reproducibility

---

### 3. Service Discovery and Networking

**Investigation**: How services communicate within Kubernetes

**Findings**:
- Kubernetes DNS automatically creates records for Services
- ClusterIP services are accessible at `<service-name>.<namespace>.svc.cluster.local`
- Short form `<service-name>` works within same namespace
- NodePort exposes service on all cluster nodes at static port (30000-32767)
- LoadBalancer requires cloud provider or MetalLB

**Decision**:
- Backend: ClusterIP service (internal DNS: `backend-service`)
- Frontend: NodePort service (external access via `minikube service`)

**Rationale**:
- Backend doesn't need external exposure
- Frontend needs external access for users/judges
- NodePort works perfectly with Minikube
- Simpler than setting up Ingress or LoadBalancer

**Implementation Notes**:
- Frontend connects to backend via `http://backend-service:8000`
- Users access frontend via `minikube service frontend-service` or `minikube-ip:30080`
- Both services in default namespace (no namespace complexity)

---

### 4. Health Probes Configuration

**Investigation**: Best practices for liveness and readiness probes in Kubernetes

**Findings**:
- Liveness probe: Detects if container is running (restart if fails)
- Readiness probe: Detects if container is ready to serve traffic
- Common probe types: HTTP GET, TCP socket, exec command
- Recommended delays: initialDelaySeconds for startup, periodSeconds for checking
- Failed liveness → pod restart; Failed readiness → removed from service endpoints

**Decision**:
- Both services use HTTP GET probes
- Backend: `/health` endpoint
- Frontend: `/` (root path)
- Conservative delays to avoid false positives during startup

**Rationale**:
- HTTP probes provide clear pass/fail signals
- Can check actual application health, not just process existence
- FastAPI and Next.js both serve HTTP naturally
- Standard industry practice

**Implementation Notes**:
- Backend needs `/health` endpoint added to FastAPI
- Frontend root path already exists
- initialDelaySeconds: 30s (allow time for startup)
- periodSeconds: 10s for liveness, 5s for readiness
- failureThreshold: 3 (3 consecutive failures trigger action)

---

### 5. Resource Limits and Requests

**Investigation**: Appropriate resource allocation for task management application

**Findings**:
- Requests: Guaranteed resources, used for scheduling
- Limits: Maximum resources, container killed if exceeded
- Best practice: Set both to prevent resource starvation and overcommitment
- Python/FastAPI: ~256-512MB typical, 0.25-0.5 CPU
- Next.js/nginx: ~128-256MB typical, 0.1-0.25 CPU

**Decision**:
- Backend: 256Mi request, 512Mi limit, 250m CPU request, 500m CPU limit
- Frontend: 128Mi request, 256Mi limit, 100m CPU request, 250m CPU limit

**Rationale**:
- Provides headroom for peak usage
- Prevents single pod from consuming all resources
- Allows 2 replicas to run comfortably on 4GB Minikube
- Based on typical resource usage patterns for these stacks

**Implementation Notes**:
- Monitor actual usage: `kubectl top pods`
- Adjust if OOMKilled or CPU throttling observed
- Conservative limits to ensure stability

---

### 6. Image Architecture (amd64 vs arm64)

**Investigation**: Platform compatibility for Docker images

**Findings**:
- Most CI/CD and cloud environments use amd64 (x86_64)
- Mac M1/M2 use arm64 (Apple Silicon)
- Docker buildx can build multi-architecture images
- Minikube runs architecture matching host by default

**Decision**: Build for linux/amd64 by default, document arm64 option

**Rationale**:
- amd64 is most widely compatible
- Judges likely using standard Intel/AMD machines
- arm64 users can rebuild for their architecture

**Implementation Notes**:
- Default: `docker build --platform linux/amd64`
- For Mac M1/M2: `docker build --platform linux/arm64`
- Can use buildx for multi-arch: `docker buildx build --platform linux/amd64,linux/arm64`

---

## Summary of Key Decisions

| Decision Area | Choice | Key Benefit |
|--------------|--------|-------------|
| Frontend Container | Multi-stage (Node + nginx) | 90% size reduction |
| Backend Service | ClusterIP | Internal-only, secure |
| Frontend Service | NodePort | Minikube-friendly external access |
| Secret Management | Kubernetes Secrets | Native, simple |
| Health Checks | HTTP probes | Application-aware |
| Database | External Neon | No state management complexity |
| Manifests | Raw YAML | Transparent, educational |
| Image Arch | linux/amd64 | Maximum compatibility |

All unknowns resolved. Ready for detailed design (data-model.md) and task breakdown.
