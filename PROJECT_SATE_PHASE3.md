# PROJECT_STATE.md

## Project Name

AI-Powered Negotiation & Sales Automation Platform

---

## 1. Project Vision

Build an AI-driven negotiation system that can:

* Conduct price negotiations with customers
* Handle multi-step offers and counter-offers
* Communicate via API-first backend (future: web, WhatsApp, telecalling)
* Track negotiation sessions, offers, and messages
* Use AI (LLM) to decide next responses and pricing strategies
* Provide dashboards and reports on AI performance

The system should behave like a **real sales agent**, following business rules first and AI reasoning second.

---

## 2. Tech Stack

### Backend

* **FastAPI** – REST APIs
* **PostgreSQL** – Primary database
* **SQLAlchemy (ORM)**
* **Alembic** – Database migrations
* **Pydantic** – Request/response schemas

### AI (Phase 3 & beyond)

* OpenAI / LLM integration
* Prompt-engineered negotiation brain
* Rule-based + AI hybrid logic

### Future Integrations

* Web dashboard (React)
* WhatsApp (Twilio / Meta API)
* Telecalling (AI voice agent)
* Analytics & reporting UI

---

## 3. Core Domain Models (Implemented)

### Customer

* id
* name
* phone / email
* created_at

### Product

* id
* name
* base_price
* min_price
* created_at

### NegotiationSession

* id
* customer_id
* product_id
* status (active, completed, failed)
* created_at

### Offer

* id
* session_id
* customer_id
* offered_price
* created_at

### Message

* id
* session_id
* sender (customer / ai)
* content
* created_at

---

## 4. Negotiation State Machine (Finalized)

### SessionStatus Enum

* active → negotiation ongoing
* completed → deal closed
* failed → negotiation ended without deal

### Rules

* Offers can only be created when session is `active`
* Offers are immutable (never updated)
* Accepting an offer sets session → `completed`
* Messages allowed only for existing sessions

---

## 5. Phase Breakdown

---

### ✅ Phase 1: Foundation (DONE)

**Status:** Completed & Stable

Includes:

* Project structure
* Database connection
* Alembic setup
* Core models & migrations
* Customers API
* Products API

---

### ✅ Phase 2: Negotiation Backend APIs (DONE)

**Status:** Completed & Tested

Includes:

* Negotiation session creation API
* Negotiation state enforcement
* Offers API (create, accept, list)
* Messages API (create & list messages)
* Proper error handling
* Database schema aligned with models

Outcome:

* Negotiation lifecycle fully functional via API

---

### 🚧 Phase 3: AI Negotiation Brain (NEXT)

**Status:** Not started

Planned components:

* AI input/output schemas
* Rule-based negotiation logic
* AI decision engine (LLM)
* AI-generated counter offers
* AI-generated message responses
* Hybrid rule + AI flow

---

### ⏳ Phase 4: Multi-Channel Integration (FUTURE)

* Web UI
* WhatsApp integration
* Telecalling (AI voice agent)
* Unified conversation tracking

---

### ⏳ Phase 5: Analytics & Admin Dashboard (FUTURE)

* Negotiation success rate
* Revenue uplift
* AI performance metrics
* Agent vs AI comparison

---

## 6. Development Rules (Strict)

* One phase at a time
* No breaking changes to completed phases
* Copy-paste safe code only
* Step-by-step execution
* Test every API before moving forward

---

## 7. Testing Status

| Component            | Status        |
| -------------------- | ------------- |
| Database connection  | ✅ OK          |
| Customers API        | ✅ Tested      |
| Products API         | ✅ Tested      |
| Negotiation sessions | ✅ Tested      |
| Offers               | ✅ Tested      |
| Messages             | ✅ Tested      |
| AI Brain             | ❌ Not started |

---

## 8. Current Focus

🎯 **Phase 3 – AI Negotiation Brain**

Next immediate goals:

1. Design AI decision flow
2. Build AI service layer
3. Integrate AI with messages & offers
4. End-to-end negotiation test with AI

---

## 9. Important Notes

* This file is the **single source of truth**
* Always paste this file when starting a new chat
* Do not redesign previous phases
* Follow step-by-step guidance only

---

## 10. Last Updated

Date: January 2026
Status: Phase 2 Completed, Phase 3 Pending
