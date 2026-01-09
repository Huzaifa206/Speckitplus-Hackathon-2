# Research: Full-Stack Web Application

## Decision: Monorepo Architecture with Strict Separation
**Rationale**: Following the Phase II constitution requirement for strict `/frontend` and `/backend` separation. This allows independent development, deployment, and scaling of each component while maintaining shared project management.

**Alternatives considered**:
- Separate repositories - rejected for increased complexity in coordination
- Single codebase without separation - rejected for violating constitution
- Micro-frontend architecture - overkill for this project scope

## Decision: Next.js 16+ with App Router
**Rationale**: Next.js App Router provides the best developer experience for building full-stack applications with built-in API routes, server components, and optimized bundling. TypeScript integration is seamless.

**Alternatives considered**:
- React with Create React App - lacks backend integration capabilities
- Vue.js/Nuxt.js - not specified in constitution
- Vanilla JavaScript - lacks framework benefits

## Decision: FastAPI for Backend
**Rationale**: FastAPI provides automatic API documentation, type validation with Pydantic, async support, and excellent performance. It integrates well with SQLModel and PostgreSQL.

**Alternatives considered**:
- Flask - lacks automatic documentation and type validation
- Django - overkill for this API-focused application
- Node.js/Express - different language stack than specified

## Decision: SQLModel ORM with Advanced Schema
**Rationale**: SQLModel combines the power of SQLAlchemy with Pydantic validation, providing type safety and automatic serialization. It's specifically mentioned in the constitution. The schema includes advanced fields like priority (enum), tags (JSON), due_date, and recurring rules to support Phase V Kafka services.

**Alternatives considered**:
- SQLAlchemy Core - lacks Pydantic integration
- Tortoise ORM - async only, doesn't match requirements
- Peewee - less feature-rich than SQLModel

## Decision: Neon Serverless PostgreSQL
**Rationale**: Neon provides serverless PostgreSQL with auto-scaling, branching, and built-in connection pooling. It's specified in the constitution and provides excellent performance for web applications. Supports the advanced schema with JSON fields for tags and proper indexing for search/filtering.

**Alternatives considered**:
- SQLite - not suitable for multi-user web application
- MongoDB - document-based, not ideal for relational task data
- MySQL - not specified in constitution

## Decision: Better Auth for Authentication
**Rationale**: Better Auth provides secure authentication with JWT tokens and integrates well with Next.js. It manages user tables automatically and supports the required user isolation and JWT verification for backend access control.

**Alternatives considered**:
- NextAuth.js - alternative auth solution but Better Auth specified
- Custom JWT implementation - security concerns and complexity
- OAuth providers only - insufficient for user isolation needs

## Decision: Shadcn-like UI with Tailwind CSS
**Rationale**: Provides clean, modern UI components with full customization capabilities. Tailwind CSS enables rapid development with consistent styling. Essential for the requested dashboard with search, filter, and sort controls.

**Alternatives considered**:
- Material UI - different aesthetic than requested
- Bootstrap - not aligned with "shadcn-like" requirement
- Vanilla CSS - lacks utility-first approach and component system

## Decision: Advanced Task Schema with Future-Proofing
**Rationale**: The task schema includes priority enum (High/Medium/Low), tags as JSON/array, due_date, and recurring fields (is_recurring, recurring_interval) as specified in the architecture. This prepares the system for Phase V Kafka services that will process recurring tasks and due dates.

**Alternatives considered**:
- Simplified schema - rejected as it wouldn't support future phases
- Different field types - JSON for tags allows flexibility, enums for priority ensure consistency