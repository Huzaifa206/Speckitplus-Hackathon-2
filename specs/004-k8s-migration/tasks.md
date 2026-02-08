# Tasks: Phase IV - Kubernetes Migration

**Feature**: 004-k8s-migration | **Date**: 2026-02-07 | **Plan**: [plan.md](./plan.md)

## Overview

This document breaks down Phase IV implementation into actionable tasks organized by user story. Each user story phase can be implemented and tested independently.

**Total Tasks**: 35
**User Stories**: 3 (P1, P2, P3)
**Parallel Opportunities**: 18 tasks marked [P]

## Implementation Strategy

**MVP Scope**: User Story 1 (P1) - Deploy application to Kubernetes
**Incremental Delivery**: Complete user stories in priority order (P1 → P2 → P3)

Each user story is independently testable:
- **US1** (P1): Deploy to Kubernetes and verify application works
- **US2** (P2): Build and publish Docker images to registry
- **US3** (P3): Configure secrets properly for production-grade setup

---

## Phase 1: Setup

**Goal**: Create Phase 4 directory structure and prepare codebase

- [x] T001 Create `/phase-4` directory structure with subdirectories: backend/, frontend/, k8s/
- [x] T002 Copy Phase III backend code from `phase-3/backend/` to `phase-4/backend/`
- [x] T003 Copy Phase III frontend code from `phase-3/frontend/` to `phase-4/frontend/`
- [x] T004 Create `phase-4/README.md` with Phase IV overview and architecture diagram
- [x] T005 Create `phase-4/k8s/README.md` with deployment instructions

**Completion Criteria**: Directory structure exists, code copied, documentation in place

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Create Docker configurations and health endpoints required for all user stories

### Backend Docker Foundation

- [x] T006 [P] [US2] Create `phase-4/backend/Dockerfile` with Python 3.9-alpine base image
- [x] T007 [P] [US2] Create `phase-4/backend/.dockerignore` excluding __pycache__, *.pyc, .env, venv/
- [x] T008 [P] [US2] Verify `phase-4/backend/requirements.txt` includes all dependencies
- [x] T009 [P] [US1] Add `/health` endpoint to `phase-4/backend/main.py` returning {"status": "healthy"}

### Frontend Docker Foundation

- [x] T010 [P] [US2] Create `phase-4/frontend/Dockerfile` with multi-stage build (Node build → nginx serve)
- [x] T011 [P] [US2] Create `phase-4/frontend/.dockerignore` excluding node_modules/, .next/, .env*
- [x] T012 [P] [US2] Update `phase-4/frontend/next.config.js` for static export if needed
- [x] T013 [P] [US2] Create `phase-4/frontend/nginx.conf` for SPA routing (all routes → index.html)

**Completion Criteria**: All Dockerfiles and configurations ready for building

---

## Phase 3: User Story 1 (P1) - Deploy Application to Kubernetes

**Story Goal**: DevOps engineer deploys entire application to local Kubernetes and verifies functionality

**Independent Test**: Run `kubectl apply -f phase-4/k8s/` followed by `minikube service frontend-service` and verify application works

### Kubernetes Manifests

- [x] T014 [US1] Create `phase-4/k8s/secret.yaml` with base64-encoded DATABASE_URL, GEMINI_API_KEY, JWT_SECRET_KEY
- [x] T015 [P] [US1] Create `phase-4/k8s/backend-deployment.yaml` with 2 replicas, resource limits, liveness/readiness probes
- [x] T016 [P] [US1] Create `phase-4/k8s/backend-service.yaml` with ClusterIP type, port 8000
- [x] T017 [P] [US1] Create `phase-4/k8s/frontend-deployment.yaml` with 2 replicas, NEXT_PUBLIC_API_URL env, probes
- [x] T018 [P] [US1] Create `phase-4/k8s/frontend-service.yaml` with NodePort type, port 3000, nodePort 30080
- [x] T019 [US1] Update frontend Deployment to reference backend via `http://backend-service:8000`

### Deployment Execution

- [ ] T020 [US1] Start Minikube cluster with `minikube start --cpus=2 --memory=4096` (MANUAL STEP)
- [ ] T021 [US1] Apply secrets: `kubectl apply -f phase-4/k8s/secret.yaml` (MANUAL STEP - requires real secrets)
- [ ] T022 [US1] Apply all manifests: `kubectl apply -f phase-4/k8s/` (MANUAL STEP)
- [ ] T023 [US1] Verify all pods reach Running status: `kubectl get pods` (MANUAL VERIFICATION)
- [ ] T024 [US1] Verify services are created: `kubectl get services` (MANUAL VERIFICATION)

### Testing & Verification

- [ ] T025 [US1] Test frontend accessibility via `minikube service frontend-service`
- [ ] T026 [US1] Test user authentication through deployed application
- [ ] T027 [US1] Test CRUD operations: create, read, update, delete tasks
- [ ] T028 [US1] Test AI chatbot functionality through deployed UI
- [ ] T029 [US1] Test self-healing: delete a backend pod and verify auto-recreation within 30 seconds
- [ ] T030 [US1] Verify tags and due dates display correctly in deployed application

**US1 Completion Criteria**:
- ✅ All pods Running
- ✅ Application accessible via Minikube
- ✅ All CRUD operations functional
- ✅ Self-healing verified

---

## Phase 4: User Story 2 (P2) - Build and Publish Docker Images

**Story Goal**: Engineer builds optimized images and publishes to Docker Hub

**Independent Test**: Run `docker build` for both services, push to Docker Hub, verify with `docker pull`

### Backend Image

- [ ] T031 [P] [US2] Build backend image: `docker build --platform linux/amd64 -t <username>/todo-backend:v1.0.0 phase-4/backend/`
- [ ] T032 [P] [US2] Test backend image locally: `docker run -p 8000:8000 -e DATABASE_URL=... <username>/todo-backend:v1.0.0`
- [ ] T033 [US2] Push backend image to Docker Hub: `docker push <username>/todo-backend:v1.0.0`
- [ ] T034 [US2] Tag and push as latest: `docker tag <username>/todo-backend:v1.0.0 <username>/todo-backend:latest && docker push <username>/todo-backend:latest`

### Frontend Image

- [ ] T035 [P] [US2] Build frontend image: `docker build --platform linux/amd64 -t <username>/todo-frontend:v1.0.0 phase-4/frontend/`
- [ ] T036 [P] [US2] Test frontend image locally: `docker run -p 3000:80 <username>/todo-frontend:v1.0.0`
- [ ] T037 [US2] Push frontend image to Docker Hub: `docker push <username>/todo-frontend:v1.0.0`
- [ ] T038 [US2] Tag and push as latest: `docker tag <username>/todo-frontend:v1.0.0 <username>/todo-frontend:latest && docker push <username>/todo-frontend:latest`

### Image Verification

- [ ] T039 [US2] Verify backend image size is < 300MB: `docker images <username>/todo-backend:v1.0.0`
- [ ] T040 [US2] Verify frontend image size is < 200MB: `docker images <username>/todo-frontend:v1.0.0`
- [ ] T041 [US2] Test pulling images from Docker Hub on clean system: `docker pull <username>/todo-backend:v1.0.0`
- [ ] T042 [US2] Update Kubernetes Deployment manifests with correct Docker Hub image names

**US2 Completion Criteria**:
- ✅ Both images built successfully
- ✅ Images under size targets
- ✅ Images pushed to Docker Hub
- ✅ Images pullable from registry

---

## Phase 5: User Story 3 (P3) - Configure Secrets and Environment Variables

**Story Goal**: Engineer configures secrets properly using Kubernetes Secrets

**Independent Test**: Apply secrets, verify pods can read env vars via `kubectl exec`

### Secret Configuration

- [ ] T043 [P] [US3] Document secret encoding process in `phase-4/k8s/README.md`
- [ ] T044 [P] [US3] Create secret encoding helper script: `phase-4/k8s/encode-secrets.sh`
- [ ] T045 [US3] Verify secret.yaml uses base64 encoding for all sensitive values
- [ ] T046 [US3] Add .gitignore entry for secret.yaml to prevent accidental commit
- [ ] T047 [US3] Create secret.yaml.example with placeholder values for documentation

### Environment Variable Configuration

- [ ] T048 [P] [US3] Verify backend Deployment uses `envFrom` to reference todo-secrets
- [ ] T049 [P] [US3] Verify frontend Deployment has NEXT_PUBLIC_API_URL environment variable
- [ ] T050 [US3] Test secret accessibility: `kubectl exec <backend-pod> -- env | grep DATABASE_URL`
- [ ] T051 [US3] Verify backend can connect to Neon database using secret credentials
- [ ] T052 [US3] Verify Gemini API works using secret API key

**US3 Completion Criteria**:
- ✅ Secrets properly encoded
- ✅ Documentation for secret management
- ✅ Pods can read secret values
- ✅ External services accessible with secrets

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Documentation, optimization, and final verification

### Documentation

- [ ] T053 [P] Create deployment guide in `phase-4/DEPLOYMENT.md` with step-by-step instructions
- [ ] T054 [P] Document troubleshooting steps in `phase-4/TROUBLESHOOTING.md`
- [ ] T055 [P] Add architecture diagram to `phase-4/README.md`
- [ ] T056 [P] Document resource requirements and Minikube setup in README

### Optimization

- [ ] T057 [P] Verify .dockerignore files minimize image sizes
- [ ] T058 [P] Optimize backend Dockerfile for layer caching
- [ ] T059 [P] Optimize frontend Dockerfile for layer caching
- [ ] T060 [P] Review and optimize resource limits in Deployments

### Final Verification

- [ ] T061 Test complete deployment from scratch following DEPLOYMENT.md
- [ ] T062 Verify all success criteria from spec.md are met
- [ ] T063 Test deployment on clean Minikube cluster
- [ ] T064 Verify pod restart time is < 30 seconds
- [ ] T065 Document any known issues or limitations in README

**Completion Criteria**: All documentation complete, optimizations applied, full system tested

---

## Dependencies & Execution Order

### User Story Dependencies

```
Setup (Phase 1) → Foundational (Phase 2) → All User Stories can proceed
                                           ├→ US1 (P1): Kubernetes Deployment
                                           ├→ US2 (P2): Image Building (required before US1)
                                           └→ US3 (P3): Secret Configuration (can run anytime)
```

**Recommended Order**:
1. Setup → Foundational
2. US2 (Build Images) → US3 (Configure Secrets) → US1 (Deploy to K8s)
3. Polish

**Parallel Execution**:
- Phase 2: Tasks T006-T013 can run in parallel (8 tasks)
- US2: Tasks T031, T032, T035, T036 can run in parallel (4 tasks)
- US3: Tasks T043-T049 can run in parallel (5 tasks)
- Polish: Tasks T053-T060 can run in parallel (8 tasks)

**Total Parallel Opportunities**: 25 tasks can be parallelized

---

## Parallel Execution Examples

### Example 1: Foundational Phase (8 parallel tasks)

```bash
# Terminal 1: Backend Docker setup
T006, T007, T008, T009

# Terminal 2: Frontend Docker setup
T010, T011, T012, T013
```

### Example 2: User Story 2 - Image Building (4 parallel tasks)

```bash
# Terminal 1: Backend image
T031 (build backend), T032 (test backend)

# Terminal 2: Frontend image
T035 (build frontend), T036 (test frontend)
```

### Example 3: Polish Phase (8 parallel tasks)

```bash
# Terminal 1: Documentation
T053, T054, T055, T056

# Terminal 2: Optimization
T057, T058, T059, T060
```

---

## Testing Checkpoints

### After Foundational Phase
- [ ] Both Dockerfiles build successfully
- [ ] Health endpoints accessible
- [ ] No syntax errors in configurations

### After US1 (Kubernetes Deployment)
- [ ] All pods reach Running status
- [ ] Services have endpoints
- [ ] Application accessible via Minikube
- [ ] Full CRUD functionality works
- [ ] Self-healing verified

### After US2 (Image Publishing)
- [ ] Images under size targets (backend < 300MB, frontend < 200MB)
- [ ] Images pullable from Docker Hub
- [ ] Deployment manifests reference correct images

### After US3 (Secret Configuration)
- [ ] Secrets properly base64-encoded
- [ ] Pods can read secret environment variables
- [ ] Database connection works with secret credentials
- [ ] API calls work with secret API keys

### Final Verification
- [ ] Complete deployment from scratch succeeds
- [ ] All success criteria from spec.md met
- [ ] Documentation complete and accurate
- [ ] No hardcoded secrets in any files

---

## Task Details by Phase

### Phase 1: Setup (5 tasks, ~15 minutes)

Creates the Phase 4 directory structure and copies existing code.

**T001-T005**: Standard directory setup, no dependencies, can be done quickly.

---

### Phase 2: Foundational (8 tasks, ~45 minutes)

Creates Docker configurations and health endpoints.

**Critical Path**: T009 (health endpoint) blocks US1 deployment testing
**Parallelizable**: All other tasks (T006-T008, T010-T013) are independent

---

### Phase 3: User Story 1 - Kubernetes Deployment (17 tasks, ~90 minutes)

Core deployment functionality.

**Critical Path**:
1. T014 (secrets) → T021 (apply secrets)
2. T015-T018 (manifests) → T022 (apply manifests)
3. T023-T024 (verify deployment) → T025-T030 (testing)

**Parallelizable**: T015-T018 (4 manifest creation tasks)

---

### Phase 4: User Story 2 - Image Building (12 tasks, ~60 minutes)

Build and publish Docker images.

**Critical Path**:
1. Backend: T031 (build) → T032 (test) → T033 (push) → T034 (tag latest)
2. Frontend: T035 (build) → T036 (test) → T037 (push) → T038 (tag latest)
3. T039-T042 (verification)

**Parallelizable**: Backend and frontend workflows are fully independent

---

### Phase 5: User Story 3 - Secret Configuration (10 tasks, ~30 minutes)

Proper secret management setup.

**Critical Path**: T045 → T050 → T051-T052 (verification)

**Parallelizable**: T043-T049 (documentation and configuration tasks)

---

### Phase 6: Polish (13 tasks, ~45 minutes)

Documentation, optimization, final verification.

**Parallelizable**: Most documentation and optimization tasks (T053-T060)
**Sequential**: Final verification tasks (T061-T065)

---

## MVP Definition

**Minimum Viable Product** = User Story 1 (P1) Complete

Tasks for MVP:
- Phase 1: All (T001-T005)
- Phase 2: All (T006-T013)
- Phase 3: All US1 tasks (T014-T030)

**MVP Deliverable**:
- Application deployed to Minikube
- All pods running
- Full CRUD functionality working
- Self-healing verified

**Total MVP Tasks**: 30 tasks
**Estimated MVP Time**: ~2.5 hours

---

## Risk Mitigation Tasks

### High Priority Risks

**Risk**: Docker image build failures
- **Task**: T032, T036 (local testing before pushing)
- **Mitigation**: Test images locally, verify dependencies

**Risk**: Kubernetes networking issues
- **Task**: T023-T024 (verify services and endpoints)
- **Mitigation**: Use kubectl describe to debug service selectors

**Risk**: Secret misconfiguration
- **Task**: T050-T052 (verify secret accessibility)
- **Mitigation**: Test secret values before full deployment

---

## Rollback Points

1. **After T013**: Can rollback to Phase III (no K8s changes yet)
2. **After T042**: Images published but not deployed (can delete from Docker Hub)
3. **After T065**: Full rollback with `kubectl delete -f phase-4/k8s/` and `minikube delete`

---

## Success Criteria Mapping

| Success Criterion | Verified By Tasks |
|-------------------|-------------------|
| SC-001: Pods Running < 2 min | T023 |
| SC-002: Services accessible | T025 |
| SC-003: CRUD operations work | T027 |
| SC-004: Self-healing < 30 sec | T029, T064 |
| SC-005: Images < 500MB | T039, T040 |
| SC-006: Startup < 3 min | T023, T025 |
| SC-007: No hardcoded secrets | T014, T046, T065 |
| SC-008: Judge reproducibility | T061, T063 |

---

## Notes

- All tasks reference Phase IV code in `/phase-4` directory
- Phase III code remains unchanged in `/phase-3`
- Docker Hub username should be consistent across all images
- Minikube must be started before any kubectl commands
- Secrets should never be committed to git
- Images should be built for linux/amd64 by default (or linux/arm64 for Mac M1/M2)

---

## Ready for Implementation

All tasks defined with:
- Clear action items
- Specific file paths
- Acceptance criteria
- Dependency relationships
- Parallel execution opportunities

Proceed with task execution starting from T001!
