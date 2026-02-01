---
id: 1
title: Constitution Update for Phase III AI Chatbot
stage: constitution
date: 2026-02-01
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 002-fullstack-web-app
user: user
command: sp.constitution
labels: [constitution, phase-iii, ai-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
---

## Prompt

```
Project: The Evolution of Todo - Phase III (AI Chatbot)
Current Phase: Phase III
Status: ACTIVE

Overview:
Transform the web application into an AI-powered system where users manage tasks via natural language.

Core Principles (Phase III):
- **Isolation**: All Phase III code MUST reside in a dedicated `/phase-3` directory. Do not modify the root `/frontend` or `/backend` from Phase II.
- **Stateless Agent**: The AI service must be stateless. Conversation history is stored in Neon DB.
- **Model Provider**: Use **Google Gemini** via the OpenAI Compatibility layer.
- **Tool-Driven**: The AI never interacts with the DB directly; it MUST use MCP Tools (`add_task`, `list_tasks`).

Active Tech Stack (Phase III):
- **Language Model**: Google Gemini (Flash 2.0 or Pro 1.5).
- **Client SDK**: OpenAI Python SDK (configured with Google Base URL).
- **Tool Protocol**: MCP (Model Context Protocol).
- **UI**: OpenAI ChatKit (Frontend).

Security Rules:
- **Secrets**: `GEMINI_API_KEY` must be loaded from `.env`.
- **Validation**: AI inputs/outputs must be sanitized.
```

## Response snapshot

Updated the project constitution to include the new Phase III requirements for the AI Chatbot:
- Added Isolation Principle
- Added Stateless Agent Principle
- Added Model Provider Constraint
- Added Tool-Driven Architecture Principle
- Updated Phase III constraints to reflect AI Chatbot requirements
- Enhanced governance section with Phase III specific rules

## Outcome

- ✅ Impact: Constitution updated to version 1.1.0 with new Phase III principles
- 🧪 Tests: Manual verification of constitution content
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Proceed with Phase III implementation following new constitution
- 🧠 Reflection: Constitution now properly reflects AI Chatbot requirements while maintaining backward compatibility

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase III implementation