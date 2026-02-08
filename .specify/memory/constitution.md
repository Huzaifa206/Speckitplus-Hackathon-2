<!-- SYNC IMPACT REPORT
Version change: 1.1.0 → 1.2.0
Modified principles: Phase IV section updated to reflect Containerization and Kubernetes requirements
Added sections: Container-First Principle (Phase IV), Orchestration Principle (Phase IV), Self-Healing Principle (Phase IV), Phase IV directory isolation
Removed sections: None
Templates requiring updates: .specify/templates/plan-template.md (✅ will update), .specify/templates/spec-template.md (✅ will update), .specify/templates/tasks-template.md (✅ will update)
Follow-up TODOs: Set up Docker Hub registry, Install Minikube locally
-->

# In-Memory Console-Based Todo Application Constitution

## Core Principles

### Simplicity First, Progressive Enhancement
Simplicity first, scalability later (progressive enhancement); Clean architecture and separation of concerns; Deterministic behavior in early phases; Extensibility for AI and cloud-native integrations; Production-grade practices introduced phase-by-phase

### Clean Architecture and Separation of Concerns
Clean architecture and separation of concerns; Code readability and maintainability prioritized; Each phase must build on the previous phase without breaking functionality

### Phase-Based Development
Each phase must build on the previous phase without breaking functionality; Technology usage must strictly follow the phase definitions; Each phase must be independently runnable; No premature optimization for future phases

### Deterministic Behavior in Early Phases
Phase I must be fully in-memory with no external persistence; Console-based interaction only in Phase I; Data stored only in runtime memory; Single-user execution; Focus on core Todo logic and command handling

### Extensibility for Future Phases
Extensibility for AI and cloud-native integrations; Configuration via environment variables only; Documentation required for every phase; No hardcoded secrets or credentials

### Isolation Principle (Phase III)
All Phase III code MUST reside in a dedicated `/phase-3` directory. Do not modify the root `/frontend` or `/backend` from Phase II.

### Stateless Agent Principle (Phase III)
The AI service must be stateless. Conversation history is stored in Neon DB.

### Model Provider Constraint (Phase III)
Use **Google Gemini** via the OpenAI Compatibility layer.

### Tool-Driven Architecture (Phase III)
The AI never interacts with the DB directly; it MUST use MCP Tools (`add_task`, `list_tasks`).

### Container-First Principle (Phase IV)
All Phase IV code (Kubernetes manifests, Dockerfiles) MUST reside in a `/phase-4` directory. Applications must run entirely from Docker images, not local development servers.

### Orchestration Principle (Phase IV)
Use Kubernetes (Minikube) to manage deployments and services. All components (frontend, backend, database) must be orchestrated via Kubernetes manifests.

### Self-Healing Principle (Phase IV)
Kubernetes configuration must allow pods to restart automatically if they crash. Implement liveness and readiness probes for all services.

## Phase Constraints

Phase I - In-Memory Python Console App: Language: Python; No database, no files, no external services; Data stored only in runtime memory; Single-user execution; Focus on core Todo logic and command handling

Phase II - Full-Stack Web Application: Frontend: Next.js; Backend: FastAPI; ORM: SQLModel; Database: Neon (PostgreSQL); REST-based API communication; Authentication-ready architecture (even if auth not implemented)

Phase III - AI-Powered Todo Chatbot:
- Isolation: All code in `/phase-3` directory
- Language Model: Google Gemini (Flash 2.0 or Pro 1.5)
- Client SDK: OpenAI Python SDK (configured with Google Base URL)
- Tool Protocol: MCP (Model Context Protocol)
- UI: OpenAI ChatKit (Frontend)
- AI Integration: Natural language interaction with Todo system
- Architecture: Statelessness with Neon DB for conversation history
- Security: Secrets via `.env` (`GEMINI_API_KEY`)

Phase IV - Containerization and Kubernetes:
- Isolation: All code in `/phase-4` directory
- Container Engine: Docker
- Orchestrator: Minikube (Local Kubernetes)
- Registry: Docker Hub (Public)
- Deployment: Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets)
- Self-Healing: Automatic pod restart on failure
- Architecture: Multi-container orchestration with service discovery
- Environment: Container-based, no local dev servers
- Operations: kubectl for deployment management
- NOT using: Helm, Vercel, Render, or serverless platforms

Phase V - Advanced Cloud Deployment: Messaging: Kafka; Service orchestration: Dapr; Cloud Provider: DigitalOcean DOKS; Microservices-ready architecture; Observability and scalability considered; Fault tolerance and async communication enabled

## Success Criteria
Phase I runs fully offline in console; Smooth transition between phases with minimal refactoring; Clean, testable, and modular codebase; AI interactions are safe, explainable, and traceable; Kubernetes and cloud deployments are reproducible; Project demonstrates end-to-end AI-native system evolution

## Governance
This constitution supersedes all other practices; Amendments require documentation, approval, and migration plan if applicable; All PRs/reviews must verify compliance with phase constraints; Complexity must be justified with clear value proposition; Each phase must be independently runnable before moving to the next phase; Code changes must follow the progressive enhancement approach from Phase I to Phase V; Phase III code must remain isolated in `/phase-3` directory; Phase IV code must remain isolated in `/phase-4` directory; AI inputs/outputs must be sanitized; Secrets must be loaded from `.env` or Kubernetes Secrets only; Container images must be tagged and versioned; Kubernetes manifests must specify resource limits and requests.

**Version**: 1.2.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-02-07