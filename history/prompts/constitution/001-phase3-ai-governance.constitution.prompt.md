---
id: 001
title: Phase 3 AI Governance Rules
stage: constitution
date: 2026-01-22
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Shahzeena Samad
command: /sp.constitution
labels: ["phase3","ai-governance","mcp-tools","agent-behavior","constitution"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - No tests for constitution update
---

## Prompt

/sp.constitution

Project: Phase III – AI-Powered Todo Chatbot using MCP & OpenAI Agents SDK

Project context:
This project is part of Hackathon II: Spec-Driven Development.
The goal is to build a stateless, scalable AI-native Todo Chatbot that manages tasks through natural language.
The system uses MCP (Model Context Protocol) tools, OpenAI Agents SDK, FastAPI backend, and a PostgreSQL database to persist state.

Core principles:
- Spec-Driven Development: All behavior must strictly follow written specifications
- Stateless Architecture: No server-side memory between requests
- Tool-First AI Design: AI agents must only act through MCP tools
- Reliability: Every user action must result in a predictable, verifiable outcome
- Clarity: Responses must be user-friendly, concise, and confirm actions clearly

Key standards:
- AI agents must never manipulate the database directly
- All task operations must go through MCP tools only
- MCP tools must be stateless and persist data via database
- Conversation state must be reconstructed from database on every request
- Agent decisions must be explainable through tool calls
- Each user intent must map to a clearly defined tool behavior

Agent behavior rules:
- When the user intent is ambiguous, prefer clarification or safe defaults
- Always confirm successful actions (create, update, delete, complete)
- On task deletion by name, list tasks first before deleting
- Gracefully handle errors such as task not found or invalid task ID
- Never hallucinate task IDs or task content
- Maintain a friendly, helpful assistant tone

MCP tool usage constraints:
- add_task: Use only when user clearly wants to create a task
- list_tasks: Use when user asks to see, show, or query tasks
- complete_task: Use only when task ID is known or confirmed
- update_task: Modify only provided fields (title/description)
- delete_task: Never delete without task identification
- Tool chaining is allowed when logically required

Data integrity rules:
- Each task must belong to the correct user_id
- Conversations must persist across requests
- Messages must be stored with correct role (user / assistant)
- No data loss on server restart

Non-goals:
- No long-term memory outside the database
- No UI logic inside the agent
- No assumptions beyond stored co

## Response snapshot

Successfully amended constitution from v1.0 to v2.0 with Phase 3 AI governance additions:

**New Core Principles Added:**
- Principle 8: Tool-First AI Design (Mandatory tool usage, no direct DB access, explainability)
- Principle 9: Agent Behavior Standards (Clarification over assumption, confirmations, safe defaults, no hallucination, friendly tone)

**New AI Governance Sections:**
- MCP Tool Usage Constraints (detailed rules for add_task, list_tasks, complete_task, update_task, delete_task with when-to-use, parameters, validation, error handling)
- Agent Behavior Rules (ambiguity handling, action confirmation templates, error handling examples, no hallucination rules, conversational tone)
- Data Integrity Rules (user data isolation, conversation persistence, no data loss on restart)

**Updated Phase III Requirements:**
- Interface: WebSocket-based chat or OpenAI ChatKit
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- Tool Architecture: All functionality through MCP tools only
- Agent Behavior: Follow tool-first design standards
- Data Integrity: User isolation and conversation persistence

All templates validated and compatible with new principles.

## Outcome

- ✅ Impact: Constitution now comprehensively governs Phase 3 AI chatbot development with tool-first design principles
- 🧪 Tests: N/A (constitution update)
- 📁 Files: Updated .specify/memory/constitution.md (v1.0 → v2.0)
- 🔁 Next prompts: Proceed with Phase 3 specification using /sp.spec
- 🧠 Reflection: Successfully integrated Phase 3 requirements into constitution without breaking existing Phase 1/2 governance. Tool-first design ensures agents remain testable, observable, and reliable.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with Phase 3 spec creation for chatbot feature
