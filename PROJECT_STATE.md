# PROJECT_STATE.md

## 1. Project Vision

This project is a **stateful AI-driven negotiation backend**.

The system enables customers to negotiate product prices through messages and offers, while strictly enforcing business rules so that:

* Negotiations are **auditable**
* History is **immutable**
* State transitions are **explicit and enforced**
* AI agents can later analyze negotiation history to decide responses

This backend is built to support **future AI automation**, not just CRUD operations.

---

## 2. Core Domain Objects (Canonical)

The following domain objects are **authoritative** and must remain consistent across:

* PostgreSQL schema
* SQLAlchemy models
* FastAPI endpoints
* Pydantic schemas
* Future AI logic

### Core Objects

* `Customer`
* `Product`
* `NegotiationSession`
* `ConversationMessage`
* `Offer`

These names must **never drift** or be duplicated with aliases.

---

## 3. Negotiation Lifecycle (State Machine)

Negotiations follow a **strict state machine**.

### Valid States

```
ACTIVE → COMPLETED | CANCELLED
```

### Rules

* A negotiation starts in `active`
* Messages can be added **only when ACTIVE**
* Offers can be created **only when ACTIVE**
* Accepting an offer moves the session to `completed`
* `completed` and `cancelled` sessions are **read-only forever**
* No object inside a closed session may be modified

State enforcement happens at **API level**, not just UI.

---

## 4. SessionStatus Enum (Single Source of Truth)

### Canonical Values (lowercase only)

```
active
completed
cancelled
```

### Rules

* PostgreSQL ENUM
* SQLAlchemy Enum
* Pydantic Enum

**Must match exactly** in spelling and case.

Any mismatch is considered a **bug**.

---

## 5. Immutability Rules (Non-Negotiable)

The following objects are **append-only**:

### ConversationMessage

* Cannot be updated
* Cannot be deleted

### Offer

* Cannot be updated
* Cannot be deleted

### NegotiationSession

* Only `status` may change
* All other fields are immutable

These rules exist to ensure:

* Auditability
* AI replay
* Legal and business safety

---

## 6. Database Reality (Current)

### Tables (PostgreSQL)

* `customers`
* `products`
* `negotiation_sessions`
* `conversation_messages`
* `offers`
* `alembic_version`

### Enum Types

* `sessionstatus`

### Migration Policy

* Schema changes are managed **only via Alembic**
* Tables must never be auto-created at runtime
* Direct SQL is allowed only for emergency recovery, then captured in Alembic

---

## 7. API Responsibilities (High-Level Contract)

### `/negotiations`

* Create negotiation session
* Transition session state (close / cancel)

### `/messages`

* Add message to ACTIVE session only
* Retrieve messages for a session (ordered)

### `/offers`

* Create offer in ACTIVE session only
* Accept offer → closes negotiation
* Retrieve offers for a session

Endpoints must **enforce state rules** — not rely on frontend behavior.

---

## 8. Error Philosophy

* Business rule violations → `400 Bad Request`
* Missing entities → `404 Not Found`
* Invalid state transitions → `400 Bad Request`
* Internal inconsistencies → `500 Internal Server Error` (must be fixed, not ignored)

Errors should be **explicit and actionable**.

---

## 9. AI Integration Contract (Future)

AI agents will:

* Read `ConversationMessage` history in order
* Read all `Offer` history
* Observe session state
* Decide next action (message / offer / accept / stop)

AI agents will **never**:

* Modify past messages
* Modify past offers
* Reopen closed sessions

The backend is designed to be **AI-safe by default**.

---

## 10. Non-Goals (Explicit)

This project does NOT aim to:

* Implement authentication (yet)
* Implement payments
* Auto-negotiate prices without human input (yet)
* Optimize prematurely

Focus is **correctness > speed**.

---

## 11. Known Current State (Living Section)

As of now:

* Alembic baseline is established
* Session status enum migration completed
* Message & offer APIs are under active stabilization
* Schema–model alignment is the top priority

This section may evolve, but earlier sections are **stable**.

---

## 12. Authority Rule

If there is ever a conflict between:

* Code
* Database
* Documentation
* Memory
* Advice

**This file wins.**

Changes to this file require **intentional decision**, not quick fixes.

---

### ✅ END OF FILE