# Requirements Specification

**Project:** Active Cyber Deception with LLM-Generated Lures  
**Document Version:** 1.0.0  
**Date:** 2026-09-23  
**Status:** Baseline  
**Author:** Project Team  
**Classification:** University Project — Internal Use

---

## Table of Contents

1. [Introduction](#1-introduction)  
   1.1 [Purpose](#11-purpose)  
   1.2 [Scope](#12-scope)  
   1.3 [Definitions and Acronyms](#13-definitions-and-acronyms)  
   1.4 [Document Overview](#14-document-overview)  
2. [Functional Requirements](#2-functional-requirements)  
   - [FR-01: Create Attacker Session](#fr-01-create-attacker-session)  
   - [FR-02: Record Requests](#fr-02-record-requests)  
   - [FR-03: Detect Suspicious Activity](#fr-03-detect-suspicious-activity)  
   - [FR-04: Calculate Risk Score](#fr-04-calculate-risk-score)  
   - [FR-05: Classify Attacker Intent](#fr-05-classify-attacker-intent)  
   - [FR-06: Generate Lure](#fr-06-generate-lure)  
   - [FR-07: Validate Lure](#fr-07-validate-lure)  
   - [FR-08: Deploy Lure](#fr-08-deploy-lure)  
   - [FR-09: Track Interaction](#fr-09-track-interaction)  
   - [FR-10: Display Events](#fr-10-display-events)  
   - [FR-11: Display Dashboard](#fr-11-display-dashboard)  
   - [FR-12: Run Attack Simulation](#fr-12-run-attack-simulation)  
3. [Non-Functional Requirements](#3-non-functional-requirements)  
   - [NFR-01: Security](#nfr-01-security)  
   - [NFR-02: Performance](#nfr-02-performance)  
   - [NFR-03: Reliability](#nfr-03-reliability)  
   - [NFR-04: Maintainability](#nfr-04-maintainability)  
   - [NFR-05: Usability](#nfr-05-usability)  
   - [NFR-06: Scalability](#nfr-06-scalability)  
   - [NFR-07: Isolation](#nfr-07-isolation)  
4. [Constraints](#4-constraints)  
5. [Assumptions](#5-assumptions)  
6. [Dependencies](#6-dependencies)

---

## 1. Introduction

### 1.1 Purpose

This document defines the complete software requirements for the **Active Cyber Deception with LLM-Generated Lures** system — a university-level cybersecurity research project that investigates the use of Large Language Models (LLMs) to automate the generation of contextually appropriate deception artefacts (lures) within a honeypot-style deception environment.

The document serves as the authoritative baseline specification for all system design, implementation, testing, and evaluation activities. It is intended for use by the development team, academic supervisors, and examiners during project review and viva assessment.

### 1.2 Scope

The system encompasses the following capabilities:

- A **Deception Environment** — a simulated web application that exposes synthetic endpoints designed to attract and engage an attacker.
- A **Session and Event Management** subsystem — tracks every attacker interaction from initial contact to lure engagement.
- A **Rule-Based Detection and Scoring Engine** — deterministically evaluates events for suspicious indicators and computes a cumulative risk score per session.
- An **Intent Classification Engine** — maps attacker behaviour patterns to a defined taxonomy of attacker intents.
- An **LLM-Powered Lure Generation Pipeline** — uses a configured LLM provider (or a deterministic mock) to produce structured, synthetic deception content tailored to the inferred attacker intent.
- A **Lure Validation and Deployment** subsystem — ensures all generated content is safe and synthetic before serving it dynamically.
- An **Operator Dashboard** — a web-based interface providing real-time visibility into attacker sessions, events, risk scores, and lure performance.
- An **Attack Simulator** — a safe, local, scriptable tool for exercising all system capabilities in a controlled manner.

The system is **entirely self-contained**. It does not connect to production networks, does not store real credentials, and does not execute LLM-generated content programmatically. All data is synthetic.

### 1.3 Definitions and Acronyms

| Term / Acronym | Definition |
|---|---|
| **LLM** | Large Language Model — an AI model capable of generating natural-language text (e.g., Ollama/Llama, OpenAI GPT). |
| **Lure** | A piece of synthetic, deceptive content (e.g., fake credentials, fabricated config files, plausible-looking API keys) deployed in the deception environment to attract and engage an attacker. |
| **Honeypot** | A decoy system or resource designed to detect, deflect, or study unauthorised access attempts. |
| **Deception Environment** | The simulated web application serving synthetic endpoints that mimic a real application to an attacker. |
| **Session** | A logical grouping of all HTTP events originating from a single attacker IP address within a defined time window. |
| **Event** | A single logged HTTP request made by an attacker to the deception environment. |
| **Risk Score** | A cumulative, deterministically computed integer value representing the threat level of an attacker session. |
| **Intent** | The inferred objective of an attacker based on their pattern of requests (e.g., RECONNAISSANCE, CREDENTIAL_DISCOVERY). |
| **Mock Provider** | A deterministic, non-LLM fallback lure generator used when the LLM endpoint is unavailable or not configured. |
| **SOC** | Security Operations Centre — the operational context this dashboard is designed to emulate. |
| **API** | Application Programming Interface. |
| **FR** | Functional Requirement. |
| **NFR** | Non-Functional Requirement. |
| **HTTP** | Hypertext Transfer Protocol. |
| **JSON** | JavaScript Object Notation. |
| **IP** | Internet Protocol address. |
| **ORM** | Object-Relational Mapper. |
| **DB** | Database. |

### 1.4 Document Overview

- **Section 2** specifies all twelve functional requirements, each with a full description, inputs, expected outputs, priority, and current status.
- **Section 3** specifies seven non-functional requirements covering security, performance, reliability, maintainability, usability, scalability, and isolation.
- **Section 4** documents fixed project constraints that the system must operate within.
- **Section 5** documents assumptions made during requirements elicitation.
- **Section 6** provides a dependency table listing all external libraries, tools, and services.

---

## 2. Functional Requirements

Each functional requirement is presented using the following schema:

| Field | Description |
|---|---|
| **ID** | Unique requirement identifier (FR-NN). |
| **Title** | Short, descriptive name. |
| **Description** | Full narrative of what the system must do. |
| **Input(s)** | Data or triggers the system receives. |
| **Output(s)** | Data or state changes the system produces. |
| **Priority** | High / Medium / Low — based on criticality to core functionality. |
| **Status** | Planned / In Progress / Implemented / Verified. |

---

### FR-01: Create Attacker Session

| Field | Value |
|---|---|
| **ID** | FR-01 |
| **Title** | Create Attacker Session |
| **Priority** | High |
| **Status** | Planned |

**Description:**

When the deception environment receives an inbound HTTP request from an IP address that does not correspond to any existing active session, the system must automatically create a new attacker session record. This session serves as the primary tracking unit for all subsequent activity originating from that source. Session creation must be atomic and must not delay the HTTP response to the attacker. The session record must be persisted to the database immediately upon creation so that it is available for all downstream processing steps (event logging, risk scoring, intent classification, and lure generation).

Session management must be transparent to the attacker — there must be no session cookie, token, or handshake that reveals the existence of the tracking mechanism. Identification is performed server-side using the source IP address as the primary key within a configurable time window. If a session for a given IP already exists and is in `active` status, the existing session must be reused rather than a new one created.

**Inputs:**

- Inbound HTTP request containing:
  - `source_ip` — the IPv4 or IPv6 address of the connecting client.
  - `user_agent` — the HTTP `User-Agent` header value (may be absent or spoofed).
  - `timestamp` — server-side datetime at which the request was received (UTC).
- System state: no existing active session record for `source_ip`.

**Outputs:**

A new session record persisted to the `sessions` database table with the following fields:

| Field | Type | Value |
|---|---|---|
| `session_id` | UUID (string) | Newly generated universally unique identifier. |
| `source_ip` | String | IP address of the attacker. |
| `user_agent` | String | Value of the HTTP `User-Agent` header, or `"unknown"` if absent. |
| `created_at` | DateTime (UTC) | Timestamp of session creation. |
| `last_seen` | DateTime (UTC) | Timestamp of most recent request (initially equal to `created_at`). |
| `risk_score` | Integer | Initial value: `0`. |
| `status` | Enum | Initial value: `"active"`. |
| `intent` | String / Null | Initial value: `null` (populated by FR-05). |

**Acceptance Criteria:**

- A unique `session_id` (UUID format) is generated for every new session.
- `risk_score` is initialised to exactly `0`.
- `status` is initialised to exactly `"active"`.
- No duplicate session is created if one already exists for the same `source_ip` with `status = "active"`.
- Session creation completes without blocking the HTTP request pipeline.

---

### FR-02: Record Requests

| Field | Value |
|---|---|
| **ID** | FR-02 |
| **Title** | Record Requests |
| **Priority** | High |
| **Status** | Planned |

**Description:**

Every HTTP request received by the deception environment must be recorded as a discrete event in the system's event log. This constitutes the primary audit trail for all attacker activity. Event recording must be comprehensive — no request may be silently dropped or omitted from the log. Each event must be linked to its parent session (created by FR-01) via the `session_id` foreign key, enabling per-session activity reconstruction.

The event record must capture sufficient context to support downstream detection (FR-03), risk scoring (FR-04), and intent classification (FR-05). This includes the requested endpoint, the HTTP method used, a server-assigned severity classification, any structured metadata relevant to the request, and the full session association. Events are immutable once written — the system must not update or delete event records, only append new ones.

**Inputs:**

- Inbound HTTP request containing:
  - `endpoint` — the URL path requested (e.g., `/admin/login`, `/.env`).
  - `method` — the HTTP verb used (`GET`, `POST`, `PUT`, `DELETE`, etc.).
  - `timestamp` — server-side UTC datetime of receipt.
  - `headers` — HTTP request headers (for metadata extraction).
  - `body` — HTTP request body, if present (for metadata extraction, e.g., submitted form fields).
- `session_id` — resolved from FR-01 for the requesting IP.
- Server-side severity classification logic (see below).

**Outputs:**

A new event record persisted to the `events` database table with the following fields:

| Field | Type | Description |
|---|---|---|
| `event_id` | UUID (string) | Unique identifier for this event. |
| `session_id` | UUID (string) | Foreign key linking to the parent session. |
| `endpoint` | String | The URL path that was requested. |
| `method` | String | The HTTP method used. |
| `timestamp` | DateTime (UTC) | Server-side time of receipt. |
| `event_type` | String | Categorical type of event (e.g., `"http_request"`, `"auth_attempt"`, `"file_access"`). |
| `severity` | Enum | One of: `"LOW"`, `"MEDIUM"`, `"HIGH"`, `"CRITICAL"`. |
| `metadata` | JSON / Dict | Structured dictionary of additional contextual data (e.g., query parameters, submitted fields, matched detection patterns). |

**Severity Assignment Rules (initial, pre-detection):**

| Severity | Criteria |
|---|---|
| `LOW` | Requests to publicly accessible, non-sensitive endpoints. |
| `MEDIUM` | Requests to endpoints that suggest probing behaviour (e.g., common discovery paths). |
| `HIGH` | Requests to administrative, credential, or configuration endpoints. |
| `CRITICAL` | Requests that match known attack patterns or trigger multiple detection rules simultaneously. |

**Acceptance Criteria:**

- Every HTTP request to the deception environment produces exactly one event record.
- Each event record has a unique `event_id` and a valid `session_id`.
- The `metadata` field is never `null`; it must at minimum be an empty JSON object `{}`.
- Event records are immutable after creation.

---

### FR-03: Detect Suspicious Activity

| Field | Value |
|---|---|
| **ID** | FR-03 |
| **Title** | Detect Suspicious Activity |
| **Priority** | High |
| **Status** | Planned |

**Description:**

The system must incorporate a rule-based detection engine that evaluates every incoming event against a defined set of detection rules. The engine must operate synchronously within the request processing pipeline and must flag events that match one or more rules as suspicious. Detection is deterministic — the same event input must always produce the same detection output. The engine must not use machine learning or probabilistic methods; all detection logic must be expressed as explicit, auditable rules.

Detection results feed directly into the risk scoring engine (FR-04) and the intent classifier (FR-05). Each triggered rule contributes a defined score increment to the session's cumulative risk score.

**Detection Rules:**

The system must implement, at minimum, the following detection rules:

| Rule ID | Rule Name | Description | Example Trigger |
|---|---|---|---|
| `RULE-001` | Admin Access Attempt | Request targets any endpoint within an `/admin` path prefix. | `GET /admin/panel` |
| `RULE-002` | Configuration File Probing | Request targets known configuration file paths or extensions. | `GET /.env`, `GET /config.php`, `GET /wp-config.php` |
| `RULE-003` | Backup File Access | Request targets paths associated with backup files or archives. | `GET /backup.zip`, `GET /db.sql`, `GET /site.tar.gz` |
| `RULE-004` | Rapid Request Rate | The session has submitted more than a configurable threshold of requests within a sliding time window. | >20 requests in 60 seconds |
| `RULE-005` | Credential Discovery Attempt | Request targets login forms, authentication endpoints, or password-related paths. | `POST /login`, `GET /api/users`, `GET /passwd` |
| `RULE-006` | Directory Traversal | Request URI contains traversal sequences. | `GET /../../etc/passwd`, `GET /files?path=../` |

**Inputs:**

- A fully formed event record (from FR-02) including `endpoint`, `method`, `session_id`, and `metadata`.
- The session's current event history (for rate-based rules).
- The configured detection rule set (loaded from application configuration).

**Outputs:**

- A list of `triggered_rules` — identifiers of all rules matched by the event (may be an empty list if no rules are triggered).
- An `is_suspicious` boolean flag: `true` if one or more rules were triggered, `false` otherwise.
- The `score_delta` — the integer score increment to be applied to the session's risk score (sum of individual rule weights).
- Updated event `metadata` annotated with the detection results.

**Acceptance Criteria:**

- All six rules listed above are implemented.
- An event that matches no rules produces `is_suspicious = false` and `score_delta = 0`.
- An event that matches multiple rules accumulates the sum of all matched rule weights.
- Detection logic is unit-testable in isolation from the HTTP request pipeline.
- Rule weights are configurable without code changes (e.g., via a configuration file or database table).

---

### FR-04: Calculate Risk Score

| Field | Value |
|---|---|
| **ID** | FR-04 |
| **Title** | Calculate Risk Score |
| **Priority** | High |
| **Status** | Planned |

**Description:**

The system must maintain a cumulative, deterministic risk score for each attacker session. The risk score is a non-negative integer that increases as the attacker triggers detection rules (FR-03). The scoring engine must be entirely deterministic — given the same sequence of events, it must always produce the same final score. The use of any LLM, machine learning model, or probabilistic method for risk score computation is strictly prohibited. This ensures auditability and reproducibility, which are fundamental requirements for a deception system used in research.

The score must be persisted to the session record after every event and must drive downstream decisions, including the lure generation trigger (FR-06). Risk scores must be mapped to discrete risk levels that determine the urgency of operator alerts and the sophistication of generated lures.

**Scoring Model:**

Risk scores are accumulated by summing the `score_delta` values produced by the detection engine (FR-03) over the lifetime of a session.

**Risk Level Classification:**

| Risk Level | Score Range | Description |
|---|---|---|
| `LOW` | 0 to 3 | Minimal suspicious activity; likely benign or exploratory traffic. |
| `MEDIUM` | 4 to 7 | Moderate suspicious activity; session warrants monitoring. |
| `HIGH` | 8 to 11 | Significant suspicious activity; session likely represents a threat actor. |
| `CRITICAL` | 12 and above | Extensive suspicious activity; session represents an active, persistent attack. |

**Default Rule Score Weights (configurable):**

| Rule ID | Rule Name | Default Score Weight |
|---|---|---|
| `RULE-001` | Admin Access Attempt | 3 |
| `RULE-002` | Configuration File Probing | 4 |
| `RULE-003` | Backup File Access | 3 |
| `RULE-004` | Rapid Request Rate | 2 |
| `RULE-005` | Credential Discovery Attempt | 4 |
| `RULE-006` | Directory Traversal | 5 |

**Inputs:**

- `session_id` — the session for which the score is being updated.
- `score_delta` — the integer increment produced by the detection engine for the current event.
- The session's current `risk_score` from the database.

**Outputs:**

- Updated `risk_score` (integer) persisted to the session record: `new_score = current_score + score_delta`.
- Derived `risk_level` (string: `"LOW"`, `"MEDIUM"`, `"HIGH"`, or `"CRITICAL"`) based on the updated score.
- The `risk_level` is exposed via the session API and displayed on the dashboard (FR-11).

**Acceptance Criteria:**

- Risk score is always a non-negative integer; it must never decrease.
- Risk level boundaries are exact: score `3` maps to `LOW`, score `4` maps to `MEDIUM`, score `8` maps to `HIGH`, score `12` maps to `CRITICAL`.
- Score computation uses no LLM, neural network, or statistical model.
- Score is recalculated and persisted after every event that produces a non-zero `score_delta`.
- Rule weights are configurable; changing a rule weight must not require a code change.

---

### FR-05: Classify Attacker Intent

| Field | Value |
|---|---|
| **ID** | FR-05 |
| **Title** | Classify Attacker Intent |
| **Priority** | High |
| **Status** | Planned |

**Description:**

The system must maintain a continuously updated classification of each attacker session's inferred primary intent. Intent classification is used to select the most contextually appropriate lure type for generation (FR-06). Classification is deterministic — it is derived from the history of events and triggered detection rules within a session, not from an LLM. The intent must be updated after each event and must reflect the dominant pattern of behaviour observed within the session.

Intent classification operates on a frequency-weighted model: the system examines the distribution of detection rule triggers across all events in a session and assigns the intent that corresponds to the most frequently triggered category. In the event of a tie, the most recently triggered intent category takes precedence.

**Intent Taxonomy:**

| Intent Value | Description | Primary Trigger Rules |
|---|---|---|
| `RECONNAISSANCE` | General information gathering; attacker is exploring the environment without a specific target. | Initial requests to root, index, or common discovery endpoints. |
| `DIRECTORY_DISCOVERY` | Attacker is systematically enumerating paths and directory structures. | `RULE-006` (directory traversal), high request volume to varied endpoints. |
| `CONFIGURATION_DISCOVERY` | Attacker is targeting configuration files, environment variables, or deployment artefacts. | `RULE-002` (configuration file probing). |
| `CREDENTIAL_DISCOVERY` | Attacker is attempting to locate or extract authentication credentials. | `RULE-005` (credential discovery), `RULE-001` (admin access). |
| `DATABASE_INTEREST` | Attacker's requests indicate interest in database access, exports, or connection strings. | `RULE-003` (backup file access with `.sql`/`.db` extensions), requests to `/db`, `/database`, `/phpmyadmin`. |
| `API_INTEREST` | Attacker is systematically probing API endpoints, keys, or documentation. | Requests to `/api/`, `/swagger`, `/openapi`, `/graphql`. |

**Inputs:**

- `session_id` — the session for which intent is being classified.
- Full event history for the session, including all triggered detection rules per event.
- The intent taxonomy table (configurable mapping of rules to intent categories).

**Outputs:**

- Updated `intent` field on the session record (one of the six intent values above, or `null` if insufficient activity).
- The `dominant_category` string representing the primary inferred intent.
- A `confidence_indicators` dictionary mapping each intent category to its trigger count (useful for debugging and dashboard display).

**Acceptance Criteria:**

- Exactly one intent value from the defined taxonomy is assigned to each session with sufficient activity.
- Intent is updated after every event.
- The classification logic is unit-testable in isolation.
- The intent value is persisted to the session record and exposed via the session API.

---

### FR-06: Generate Lure

| Field | Value |
|---|---|
| **ID** | FR-06 |
| **Title** | Generate Lure |
| **Priority** | High |
| **Status** | Planned |

**Description:**

When an attacker session reaches a defined risk score threshold and has a classified intent, the system must automatically invoke the lure generation pipeline to produce a contextually appropriate synthetic deception artefact (lure). The lure must be tailored to the attacker's inferred intent so that it is plausible and likely to engage the attacker's interest, thereby extending dwell time within the controlled deception environment.

The lure generation pipeline must support two provider modes:

1. **LLM Provider Mode:** The system sends a structured prompt to a configured LLM API endpoint (e.g., Ollama running a local model, or OpenAI-compatible API). The prompt includes the attacker's `intent`, `risk_score`, `risk_level`, and a sample of recent events. The LLM generates a JSON-structured lure response.
2. **Mock Provider Mode:** A deterministic, pre-programmed function generates a lure based solely on the `intent` value, without any LLM call. This mode is used when the LLM endpoint is unavailable, not configured, or when running in offline/test environments.

The pipeline must be designed so that switching between LLM and mock modes requires only a configuration change, with no code modification.

**Lure Types by Intent (minimum set):**

| Intent | Lure Type | Example Lure Content |
|---|---|---|
| `RECONNAISSANCE` | `fake_admin_panel` | Fabricated admin login page with fake credentials. |
| `DIRECTORY_DISCOVERY` | `fake_directory_listing` | Synthetic directory index with enticing filenames. |
| `CONFIGURATION_DISCOVERY` | `fake_config_file` | Plausible-looking `.env` file with synthetic keys and values. |
| `CREDENTIAL_DISCOVERY` | `fake_credentials` | Fabricated username/password pairs with realistic formatting. |
| `DATABASE_INTEREST` | `fake_database_dump` | Synthetic SQL dump snippet with realistic but fictional schema and data. |
| `API_INTEREST` | `fake_api_keys` | Fabricated API key strings in realistic formats. |

**Inputs:**

- `session_id` — the attacker session triggering lure generation.
- `intent` — the classified attacker intent (from FR-05).
- `risk_score` — the session's current risk score (from FR-04).
- `risk_level` — derived risk level string.
- `recent_events` — a list of the most recent events from the session (for prompt enrichment).
- `provider_mode` — configuration value: `"llm"` or `"mock"`.
- LLM endpoint configuration (if `provider_mode = "llm"`): base URL, model name, timeout.

**Outputs:**

A structured JSON lure object conforming to the following schema:

```json
{
  "lure_type":    "<string>  — one of the defined lure types",
  "title":        "<string>  — a short, descriptive title for the lure",
  "content":      "<string>  — the body of the lure (synthetic deceptive content)",
  "interest":     "<string>  — the attacker intent this lure targets",
  "confidence":   "<float>   — 0.0 to 1.0, provider's confidence in lure relevance",
  "provider":     "<string>  — 'llm' or 'mock', indicating which provider generated the lure",
  "generated_at": "<datetime>— UTC timestamp of generation"
}
```

**Acceptance Criteria:**

- Lure generation is triggered automatically when `risk_score >= configurable_threshold` and `intent` is not `null`.
- The generated lure object always contains all required fields: `lure_type`, `title`, `content`, `interest`, `confidence`.
- In mock mode, lure generation is synchronous and deterministic (same `intent` always produces structurally equivalent output).
- In LLM mode, the system correctly handles timeout, API errors, and malformed responses by falling back to mock mode and logging the failure.
- The raw LLM response is validated by FR-07 before the lure is deployed; unvalidated LLM output is never used directly.

---

### FR-07: Validate Lure

| Field | Value |
|---|---|
| **ID** | FR-07 |
| **Title** | Validate Lure |
| **Priority** | High |
| **Status** | Planned |

**Description:**

Every lure produced by the generation pipeline (FR-06), regardless of provider mode, must pass through a deterministic validation layer before it is deployed to the deception environment. This requirement exists to guarantee that no harmful, real, or executable content is ever served to an attacker, even in the event of a compromised or adversarially manipulated LLM response. The validator is a critical security control: it must be the last gate before any lure content is written to the database or served via an HTTP endpoint.

The validator must be implemented as a standalone, testable component with no dependency on the LLM. It applies a series of rule-based checks to the lure object and either approves it (with an optional set of warnings) or rejects it (with a descriptive reason). Rejected lures must never be deployed; the system must fall back to the mock provider and re-validate, or discard lure generation for the session and retry on the next event.

**Validation Rules:**

| Rule ID | Check | Rejection Condition |
|---|---|---|
| `VAL-001` | Required Fields Present | Any of `lure_type`, `title`, `content`, `interest`, `confidence` is absent or `null`. |
| `VAL-002` | No Executable Commands | `content` contains shell command patterns: backtick expressions, `$(...)`, `exec(`, `eval(`, `system(`, `subprocess`, `os.system`. |
| `VAL-003` | No Real Secrets | `content` contains patterns matching real credentials: valid AWS key prefixes (`AKIA...`), GitHub personal access tokens (`ghp_...`), PEM header (`-----BEGIN`), high-entropy strings matching known secret formats. |
| `VAL-004` | Content Length Limits | `content` length is less than 10 characters (too short to be meaningful) or exceeds 10,000 characters (excessively large; likely a generation error). |
| `VAL-005` | Content is Synthetic | `content` does not contain live domain names, real IP addresses (non-RFC-1918 ranges), or identifiable personal information. |
| `VAL-006` | Lure Type is Known | `lure_type` value is a member of the defined lure type enumeration. |
| `VAL-007` | Confidence is Valid | `confidence` is a float in the range [0.0, 1.0]. |

**Inputs:**

- The raw lure object produced by FR-06 (JSON dictionary).

**Outputs:**

- `is_valid` — boolean: `true` if all validation rules pass, `false` if any rule fails.
- `validation_errors` — list of strings describing each failed rule (empty if `is_valid = true`).
- `validation_warnings` — list of strings describing near-violations or quality notes (non-blocking).
- `validated_lure` — the lure object, unchanged, if `is_valid = true`; `null` if `is_valid = false`.

**Acceptance Criteria:**

- Every lure produced by FR-06 is validated before deployment; no exceptions.
- A lure that fails any single rule is rejected; partial approval is not permitted.
- Validation of a lure containing a real AWS key (`AKIA...`) always results in `is_valid = false`.
- Validation of a lure containing `eval(` always results in `is_valid = false`.
- Validation executes without making any external network calls.
- All seven validation rules have corresponding unit tests.

---

### FR-08: Deploy Lure

| Field | Value |
|---|---|
| **ID** | FR-08 |
| **Title** | Deploy Lure |
| **Priority** | High |
| **Status** | Planned |

**Description:**

Once a lure has passed validation (FR-07), it must be dynamically deployed into the deception environment so that it is accessible to the attacker. Deployment means registering the lure as an active, accessible HTTP endpoint within the deception environment and persisting its full record to the database. The attacker must be able to request the lure endpoint and receive the lure content in a response that appears natural and consistent with the simulated application.

Deployment must be dynamic — lures are not statically defined at application startup. New lures are added to the routing table at runtime, without requiring a server restart. Each lure must be accessible at a URL path that is contextually consistent with the lure type (e.g., a fake config file lure should be accessible at a path like `/.env` or `/config/app.env`).

**Inputs:**

- `validated_lure` — the fully validated lure object from FR-07.
- `session_id` — the session for which the lure was generated.
- `deployment_path` — the URL path at which the lure will be served (derived from `lure_type` or assigned dynamically).

**Outputs:**

A new lure record persisted to the `lures` database table with the following fields:

| Field | Type | Description |
|---|---|---|
| `lure_id` | UUID (string) | Unique identifier for this lure. |
| `session_id` | UUID (string) | Foreign key to the generating session. |
| `lure_type` | String | The type of lure (from the validated lure object). |
| `title` | String | The lure title. |
| `content` | String | The synthetic lure content. |
| `interest` | String | The attacker intent this lure targets. |
| `confidence` | Float | Provider's confidence score. |
| `provider` | String | `"llm"` or `"mock"`. |
| `deployment_path` | String | The URL path at which the lure is served. |
| `deployed_at` | DateTime (UTC) | Timestamp of deployment. |
| `status` | Enum | `"active"` initially; transitions to `"interacted"` when accessed (FR-09). |
| `interaction_count` | Integer | Number of times the lure has been accessed. Initially `0`. |

- The lure endpoint is registered in the deception environment's routing table and becomes accessible at `deployment_path`.

**Acceptance Criteria:**

- No lure may be deployed unless it has passed FR-07 validation.
- The deployed endpoint serves the lure content with an appropriate HTTP Content-Type header (e.g., `text/plain` for config files, `application/json` for API key lures).
- Deployment is persisted to the database before the endpoint is registered.
- Duplicate deployment to the same `deployment_path` is handled gracefully (e.g., by versioning or overwriting, per configuration).

---

### FR-09: Track Interaction

| Field | Value |
|---|---|
| **ID** | FR-09 |
| **Title** | Track Interaction |
| **Priority** | High |
| **Status** | Planned |

**Description:**

When an attacker accesses a deployed lure endpoint, the system must record the interaction as a discrete, traceable event. Lure interaction tracking provides the primary measure of deception effectiveness — it demonstrates whether generated lures successfully engaged the attacker. Each interaction must be associated with both the lure and the attacker session, and must capture sufficient metadata to support downstream analysis of attacker behaviour.

An interaction event is distinct from a standard event record (FR-02), although it may also generate a corresponding standard event record. The interaction record must be persisted to a dedicated `lure_interactions` table and must trigger an update to the lure's `interaction_count` and `status` fields. Interactions must also contribute to the session's risk score (configurable score delta for lure engagement).

**Interaction Types:**

| Interaction Type | Description |
|---|---|
| `view` | Attacker made a `GET` request to the lure endpoint and received the lure content. |
| `download` | Attacker made a request that resulted in a file download (Content-Disposition: attachment). |
| `submit` | Attacker submitted data to a lure endpoint (e.g., POST to a fake login form). |

**Inputs:**

- `lure_id` — the UUID of the lure that was accessed.
- `session_id` — the UUID of the attacker session making the request.
- `interaction_type` — derived from the HTTP method and lure type (`"view"`, `"download"`, `"submit"`).
- `timestamp` — server-side UTC datetime of the interaction.
- `metadata` — additional context: HTTP method, query parameters, submitted body (for `submit` type), response code served.

**Outputs:**

A new interaction record persisted to the `lure_interactions` table:

| Field | Type | Description |
|---|---|---|
| `interaction_id` | UUID (string) | Unique identifier for this interaction. |
| `lure_id` | UUID (string) | Foreign key to the accessed lure. |
| `session_id` | UUID (string) | Foreign key to the attacker session. |
| `interaction_type` | String | One of: `"view"`, `"download"`, `"submit"`. |
| `timestamp` | DateTime (UTC) | Time of the interaction. |
| `metadata` | JSON / Dict | Additional contextual data. |

Additional outcomes:

- The lure record's `interaction_count` is incremented by 1.
- The lure record's `status` is updated to `"interacted"` (if not already).
- A corresponding standard event record is created via FR-02 with `event_type = "lure_interaction"` and `severity = "HIGH"`.

**Acceptance Criteria:**

- Every access to a deployed lure endpoint produces exactly one interaction record.
- Interaction records are immutable after creation.
- The lure's `interaction_count` reflects the true cumulative count of all interaction records for that `lure_id`.
- Interaction tracking does not reveal to the attacker that they have engaged with a lure.

---

### FR-10: Display Events

| Field | Value |
|---|---|
| **ID** | FR-10 |
| **Title** | Display Events |
| **Priority** | Medium |
| **Status** | Planned |

**Description:**

The operator dashboard must include a dedicated Events page that provides a real-time, tabular view of all events recorded in the deception environment. The Events page is the primary investigative interface for security operators, allowing them to review attacker activity at the individual request level. The page must present events in a format that is immediately scannable, with the most critical information visible without requiring the operator to navigate to a detail view.

The Events page must support filtering and sorting to allow operators to focus on specific sessions, severity levels, or time ranges. All data displayed is read-only; operators must not be able to modify event records from this interface.

**Displayed Fields (per event row):**

| Column | Description |
|---|---|
| **Endpoint** | The URL path that was requested. |
| **Event Type** | Categorical type of the event. |
| **Severity** | Colour-coded severity badge (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`). |
| **Timestamp** | UTC datetime, formatted as `YYYY-MM-DD HH:MM:SS`. |
| **Session ID** | Truncated session UUID with a link to the session detail view. |

**Filtering and Sorting:**

- **Filter by Severity:** Operator can select one or more severity levels to display.
- **Filter by Session ID:** Operator can enter a partial or full session ID to isolate events from one session.
- **Filter by Time Range:** Operator can specify a start and end datetime to restrict the displayed event set.
- **Sort by Timestamp:** Ascending and descending; default is descending (most recent first).
- **Sort by Severity:** Allows grouping by impact.

**Inputs:**

- Query parameters from the operator's browser: filter criteria and sort preferences.
- Event records from the database.

**Outputs:**

- A rendered HTML page (or dynamically updated web component) displaying a paginated table of events matching the active filter criteria.
- Pagination controls with configurable page size (default: 50 events per page).

**Acceptance Criteria:**

- All five required columns are displayed for every event row.
- Severity badges are visually differentiated by colour (at minimum: `HIGH` and `CRITICAL` use a distinct warning colour).
- Default view shows the 50 most recent events, ordered by timestamp descending.
- Filter and sort operations do not cause a full page reload (client-side filtering preferred, or fast AJAX call).
- The page renders within 3 seconds under normal load conditions.

---

### FR-11: Display Dashboard

| Field | Value |
|---|---|
| **ID** | FR-11 |
| **Title** | Display Dashboard |
| **Priority** | Medium |
| **Status** | Planned |

**Description:**

The system must provide a web-based operator dashboard that serves as the primary interface for monitoring the deception environment in real time. The dashboard's overview page (index/home) must present a high-level summary of current system activity, allowing a security operator to quickly assess the state of the deception operation without needing to navigate to individual session or event records.

The dashboard must adopt a SOC-style dark-themed visual design to reflect the operational context of a security operations centre. All metrics must be drawn live from the database and must reflect the current state of the system. The dashboard must auto-refresh or support manual refresh to keep metrics current.

**Metrics Displayed:**

| Metric | Description |
|---|---|
| **Active Sessions** | Count of sessions with `status = "active"`. |
| **Suspicious Events** | Count of events where `is_suspicious = true` (i.e., at least one detection rule was triggered). |
| **High-Risk Sessions** | Count of sessions with `risk_level` of `"HIGH"` or `"CRITICAL"`. |
| **Generated Lures** | Total count of lure records in the database. |
| **Lure Interactions** | Total count of records in the `lure_interactions` table. |
| **Attack Stage Distribution** | A visual breakdown (e.g., bar chart or pie chart) showing the distribution of session intents across the six intent categories. |

**Additional Dashboard Features:**

- A recent activity feed showing the last 10 events across all sessions.
- A sessions summary table showing the top 5 sessions by risk score, with columns for `session_id`, `source_ip`, `risk_score`, `risk_level`, and `intent`.
- Navigation links to the Events page (FR-10) and individual session detail views.

**Inputs:**

- Aggregated query results from the `sessions`, `events`, `lures`, and `lure_interactions` database tables.

**Outputs:**

- A rendered HTML dashboard page with all six metrics and supporting visualisations.

**Acceptance Criteria:**

- All six metrics are displayed simultaneously on the overview page.
- The attack stage distribution chart renders correctly with data from all six intent categories.
- The dashboard uses a dark colour theme (dark background, light text).
- The page loads within 3 seconds under normal operating conditions.
- Metrics are accurate within one database query cycle (no stale data older than the last page load).

---

### FR-12: Run Attack Simulation

| Field | Value |
|---|---|
| **ID** | FR-12 |
| **Title** | Run Attack Simulation |
| **Priority** | Medium |
| **Status** | Planned |

**Description:**

The system must include a safe, local, scriptable attack simulator that is capable of exercising the full end-to-end deception pipeline without any human attacker or external tooling. The simulator must operate entirely within the local Docker network, targeting only the deception environment container, and must never make requests to external systems. It is used for demonstration, testing, and evaluation purposes.

The simulator must implement a set of predefined attack scenarios, each representing a realistic attacker behavioural pattern. Each scenario is a scripted sequence of HTTP requests to the deception environment. The simulator must be executable from the command line and must produce a human-readable output log of all requests sent and responses received.

**Predefined Attack Scenarios:**

| Scenario ID | Scenario Name | Description | Example Requests |
|---|---|---|---|
| `SIM-001` | Basic Reconnaissance | Initial probing with general discovery requests. | `GET /`, `GET /robots.txt`, `GET /sitemap.xml`, `GET /index.html` |
| `SIM-002` | Admin Discovery | Targeted enumeration of administrative endpoints. | `GET /admin`, `GET /admin/login`, `GET /admin/users`, `POST /admin/login` |
| `SIM-003` | Configuration Discovery | Probing for exposed configuration and environment files. | `GET /.env`, `GET /config.php`, `GET /wp-config.php`, `GET /config/database.yml` |
| `SIM-004` | Credential Discovery | Searching for authentication credentials and user data. | `GET /api/users`, `GET /api/keys`, `POST /login`, `GET /passwd` |
| `SIM-005` | Database-Focused Attack | Targeting database files, exports, and connection strings. | `GET /backup.sql`, `GET /db.sqlite`, `GET /phpmyadmin`, `GET /api/db/dump` |

**Inputs:**

- Command-line argument: the scenario ID to execute (e.g., `python simulator.py --scenario SIM-002`), or `--all` to run all scenarios sequentially.
- Configuration: the base URL of the deception environment (default: `http://localhost:5001`).
- Optional: `--delay <seconds>` to introduce a configurable inter-request delay simulating realistic attacker pacing (default: 0.5s).

**Outputs:**

- A console log of each request sent, formatted as: `[TIMESTAMP] [METHOD] [URL] -> HTTP [STATUS_CODE]`.
- A summary report at the end of each scenario execution showing: total requests sent, events generated, risk score achieved, intent classified, and lures generated.
- Optional: a JSON output file (`--output <file>`) containing the full structured simulation report.

**Acceptance Criteria:**

- All five scenarios execute without errors against a running deception environment instance.
- Executing `SIM-003` (Configuration Discovery) triggers at minimum one lure generation cycle.
- Executing `SIM-004` (Credential Discovery) results in a session `intent` of `CREDENTIAL_DISCOVERY`.
- The simulator does not make any requests outside the configured deception environment base URL.
- Simulator execution is idempotent with respect to the deception environment — each run creates a fresh session (due to configurable source IP spoofing or distinct run identifiers).

---

## 3. Non-Functional Requirements

### NFR-01: Security

| Field | Value |
|---|---|
| **ID** | NFR-01 |
| **Title** | Security |
| **Priority** | High |
| **Status** | Planned |

**Requirements:**

1. **All Data is Synthetic:** The system must never store, process, or transmit real credentials, real IP addresses from production systems, real API keys, or any personally identifiable information. All data in the database is either generated by the system itself or provided by the attack simulator using synthetic values.

2. **LLM Output is Never Executed:** Content produced by the LLM provider must never be executed as code, interpreted as a command, or used in a context where it could affect system state outside the deception environment. LLM output is treated as untrusted user input and must always pass through the lure validator (FR-07) before use.

3. **No Real Credentials in Lures:** The lure validator (FR-07) must enforce that no lure content contains patterns matching real secret formats. This is a hard security control, not a best-effort check.

4. **Docker Network Isolation:** All system components must run within a Docker Compose network. No component may expose unnecessary ports to the host network. The deception environment and backend service ports must be limited to those strictly necessary for system operation and operator access.

5. **Dashboard Authentication:** The operator dashboard must implement basic authentication to prevent unauthorised access. In a university context, HTTP Basic Auth with a configurable username/password pair is acceptable; production deployment would require stronger authentication.

6. **No Inbound Connections from External Networks:** The deception environment must only be accessible within the local Docker network (and optionally `localhost`). It must not be exposed to the public internet.

---

### NFR-02: Performance

| Field | Value |
|---|---|
| **ID** | NFR-02 |
| **Title** | Performance |
| **Priority** | Medium |
| **Status** | Planned |

**Requirements:**

| Metric | Requirement |
|---|---|
| **Event Processing Latency** | The pipeline from receiving an HTTP request to completing event persistence, detection, and risk score update must complete in under **100 milliseconds** (excluding LLM generation time). |
| **LLM Lure Generation Time** | Lure generation via an LLM provider must complete within **30 seconds**. If the LLM does not respond within this timeout, the system must fall back to the mock provider. |
| **Dashboard Page Load Time** | The operator dashboard overview page must fully render within **3 seconds** under normal operating conditions (up to 10 active sessions, up to 1000 events in the database). |
| **Concurrent Session Support** | The system must correctly handle at least **10 concurrently active simulated attacker sessions** without data corruption or significant performance degradation. |
| **Database Query Performance** | All database queries for dashboard metrics must complete in under **500 milliseconds**. |

---

### NFR-03: Reliability

| Field | Value |
|---|---|
| **ID** | NFR-03 |
| **Title** | Reliability |
| **Priority** | High |
| **Status** | Planned |

**Requirements:**

1. **Graceful LLM Degradation:** If the configured LLM provider is unavailable (network error, timeout, API error), the system must automatically fall back to the mock lure provider. The fallback must be transparent to the operator except for a logged warning and a `provider: "mock"` indicator on the generated lure record. The system must never crash or return a 500 error to the deception environment due to an LLM failure.

2. **Database Transaction Integrity:** All multi-step database operations (e.g., creating a session and recording the first event, deploying a lure and registering its endpoint) must be wrapped in database transactions. If any step fails, the transaction must be rolled back to prevent partial writes.

3. **API Error Handling:** Every HTTP API endpoint exposed by the backend must handle all anticipated error conditions (invalid input, missing records, database errors) and return a structured JSON error response with an appropriate HTTP status code. Unhandled exceptions must be caught by a global error handler that returns a `500` response with a generic error message, without exposing internal stack traces.

4. **Startup Resilience:** The system must correctly handle a cold start where the database is empty. All dashboard metrics must gracefully display `0` rather than raising errors when no data exists.

5. **Lure Deployment Failure Handling:** If lure deployment fails (e.g., due to a database write error), the system must log the failure, not crash, and the deception environment must continue operating normally for subsequent requests.

---

### NFR-04: Maintainability

| Field | Value |
|---|---|
| **ID** | NFR-04 |
| **Title** | Maintainability |
| **Priority** | Medium |
| **Status** | Planned |

**Requirements:**

1. **Clean Architecture and Separation of Concerns:** The backend codebase must be organised into clearly separated layers: API layer (route handlers), service layer (business logic), data access layer (database operations), and utility/helper modules. No business logic may reside directly in route handler functions.

2. **Type Hints:** All Python functions and methods must include PEP 484-compliant type annotations for parameters and return values.

3. **Modular Code:** The detection engine, scoring engine, intent classifier, lure generator, and lure validator must each be implemented as independent, separately importable modules. A change to one module must not require changes to another, except via its defined interface.

4. **Test Coverage:** The backend service must achieve a minimum of **80% line coverage** as measured by `pytest-cov`. All critical components — detection rules, scoring logic, validation rules, intent classification — must have dedicated unit tests.

5. **Configuration-Driven Behaviour:** Rule weights, risk level thresholds, lure generation triggers, LLM provider settings, and simulator parameters must be configurable via environment variables or a configuration file. No magic numbers directly in source code.

6. **Code Documentation:** All public modules, classes, and functions must have docstrings explaining their purpose, parameters, and return values.

---

### NFR-05: Usability

| Field | Value |
|---|---|
| **ID** | NFR-05 |
| **Title** | Usability |
| **Priority** | Medium |
| **Status** | Planned |

**Requirements:**

1. **SOC-Style Dark-Themed Dashboard:** The operator dashboard must use a dark colour scheme (dark background, light/neutral text, accent colours for status indicators). The design must evoke the visual language of professional SOC tooling (e.g., Splunk, Kibana dark mode).

2. **Responsive UI:** The dashboard must render correctly on screen widths from 1024px to 2560px (desktop/monitor range). Mobile responsiveness is desirable but not required.

3. **Clear Status Indicators:** Risk levels (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) and session/lure statuses must be represented with colour-coded badges that communicate severity without requiring the operator to read the text value. At minimum: green for LOW, yellow/amber for MEDIUM, orange for HIGH, red for CRITICAL.

4. **Intuitive Navigation:** The dashboard must provide a consistent navigation structure (e.g., sidebar or top navigation bar) with links to all major sections: Overview, Events, Sessions. The currently active section must be visually highlighted.

5. **Self-Describing Event Log:** The Events page (FR-10) must present events in a format that is immediately interpretable without requiring additional context. Column headers must be clearly labelled.

---

### NFR-06: Scalability

| Field | Value |
|---|---|
| **ID** | NFR-06 |
| **Title** | Scalability |
| **Priority** | Low |
| **Status** | Planned |

**Requirements:**

1. **Database Abstraction Layer:** All database operations must be performed via an ORM (e.g., SQLAlchemy) with a database-agnostic query interface. The system must use SQLite for the development and demonstration deployment, but the abstraction layer must allow migration to PostgreSQL without changes to business logic or service layer code.

2. **API Pagination:** All list-returning API endpoints (events, sessions, lures, interactions) must support `page` and `page_size` query parameters. Unpaginated responses that return all records from a large table are not acceptable for production scalability.

3. **Configurable Scoring Rules:** The detection rule set and associated score weights must be loadable from a configuration source (file or database table) at runtime, allowing new rules to be added without code deployment.

4. **Stateless Backend Service:** The backend API service must be stateless (all session and event state is in the database) to allow horizontal scaling via multiple container replicas, should the system be deployed in a scaled environment.

---

### NFR-07: Isolation

| Field | Value |
|---|---|
| **ID** | NFR-07 |
| **Title** | Isolation |
| **Priority** | High |
| **Status** | Planned |

**Requirements:**

1. **All Components in Docker:** Every system component — the backend service, the deception environment, the database, and the LLM provider (if self-hosted via Ollama) — must run as a Docker container defined in a `docker-compose.yml` file. No component may require installation directly on the host operating system (beyond Docker and Docker Compose themselves).

2. **No Unsanctioned External Network Calls:** The only permitted external network call is to the configured LLM API endpoint. All other outbound network traffic from system containers is prohibited. This must be enforced by Docker network configuration (using an isolated bridge network with no default internet route, or by ensuring the Ollama LLM container is also within the Compose network).

3. **Deception Environment Isolated from Real Infrastructure:** The deception environment must have no access to any real application database, real file system sensitive data, or real internal network services. It must operate entirely on synthetic data served from its own application layer.

4. **Attack Simulator Confined to Compose Network:** The attack simulator container must only be able to reach the deception environment container by its Docker Compose service name and internal port. It must have no route to the host network or external internet.

5. **Volume-Based Data Persistence:** Database files and log files must be stored in Docker named volumes, not bind-mounted to arbitrary host paths, to ensure isolation between the containerised system and the host file system.

---

## 4. Constraints

The following fixed constraints apply to the project and cannot be changed without explicit supervisor approval:

| ID | Constraint | Rationale |
|---|---|---|
| **C-01** | The system must run entirely on a single developer machine (minimum: 8 GB RAM, quad-core CPU) using Docker Compose. No cloud infrastructure or external servers are permitted. | University project scope; budget and ethics constraints. |
| **C-02** | The LLM must be run locally (e.g., via Ollama) or accessed via a locally configured API endpoint. No calls to paid cloud LLM APIs are made in the production demonstration unless explicitly approved and funded. | Cost, data privacy, and offline demonstration requirements. |
| **C-03** | The system must not be connected to any real network beyond `localhost`. | Ethical and safety requirement; prevents the deception environment from accidentally engaging real attackers. |
| **C-04** | The backend must be implemented in Python (version 3.10+). | Team proficiency and ecosystem compatibility. |
| **C-05** | The frontend dashboard must be a web-based interface (HTML/CSS/JavaScript). Standalone desktop applications are not permitted. | Accessibility and demonstration requirements. |
| **C-06** | The primary database for development and demonstration must be SQLite. PostgreSQL migration capability is required (NFR-06) but not demonstrated in the submission. | Simplicity of deployment; no external database server required. |
| **C-07** | Risk scoring (FR-04) must be entirely deterministic and must not use any LLM, neural network, or statistical model. | Academic integrity requirement; the scoring mechanism must be fully auditable and explainable. |
| **C-08** | All lure content must be synthetic and clearly fabricated. No real credentials, real system information, or real user data may be used in any lure. | Ethical requirement; using real sensitive data as lures would constitute a security vulnerability. |

---

## 5. Assumptions

The following assumptions were made during requirements elicitation and must be validated prior to final submission:

| ID | Assumption |
|---|---|
| **A-01** | The development machine has Docker Desktop and Docker Compose installed and configured. |
| **A-02** | An Ollama instance with a suitable model (e.g., `llama3.2`, `mistral`) is available on the local network or within the Docker Compose network. If Ollama is not available, the mock provider (FR-06) provides sufficient functionality for all evaluation scenarios. |
| **A-03** | The attack simulator (FR-12) is sufficient to exercise all system capabilities without requiring a real attacker or third-party penetration testing tools (e.g., `nmap`, `Burp Suite`). |
| **A-04** | SQLite's write concurrency limitations are acceptable for the maximum of 10 concurrent simulated sessions (NFR-02). Higher concurrency would require PostgreSQL. |
| **A-05** | The operator dashboard does not need to support real-time push updates (e.g., WebSocket). Page-level refresh or periodic polling is sufficient for the evaluation context. |
| **A-06** | The LLM model used for lure generation has been pre-downloaded and is available in the Ollama model library at the time of demonstration. No internet connectivity is assumed during the live demonstration. |
| **A-07** | The deception environment simulates a web application; it does not need to simulate other protocol-level honeypots (e.g., SSH, FTP, SMB). |
| **A-08** | Session identification based on source IP address is sufficient for the simulation context. In a real deployment, more sophisticated session tracking (e.g., TLS fingerprinting, JA3 hashing) would be required. |
| **A-09** | The term "attacker" refers exclusively to the scripted attack simulator (FR-12) in all evaluation and demonstration contexts. No actual human attacker is involved. |

---

## 6. Dependencies

The following external libraries, tools, frameworks, and services are required for the system. All dependencies must be pinned to specific versions in the project's `requirements.txt` (Python) and `package.json` (JavaScript, if applicable) files to ensure reproducible builds.

### 6.1 Backend Python Dependencies

| Package | Version (approx.) | Purpose |
|---|---|---|
| `Flask` | >= 2.3 | Web framework for the backend API and deception environment HTTP server. |
| `SQLAlchemy` | >= 2.0 | ORM and database abstraction layer for SQLite (and future PostgreSQL). |
| `Flask-SQLAlchemy` | >= 3.0 | Flask integration for SQLAlchemy. |
| `requests` | >= 2.31 | HTTP client used by the backend to call the LLM API (Ollama/OpenAI-compatible). |
| `pydantic` | >= 2.0 | Data validation and schema definition for API request/response models and lure schema. |
| `python-dotenv` | >= 1.0 | Loading environment variable configuration from `.env` files. |
| `pytest` | >= 7.0 | Unit and integration testing framework. |
| `pytest-cov` | >= 4.0 | Test coverage measurement plugin for pytest. |
| `Jinja2` | >= 3.1 | HTML template engine (used by Flask for dashboard rendering). |
| `Werkzeug` | >= 3.0 | WSGI utility library (Flask dependency; also used for password hashing for basic auth). |
| `uuid` | stdlib | UUID generation for session, event, lure, and interaction identifiers. |

### 6.2 Frontend Dependencies

| Dependency | Version (approx.) | Purpose |
|---|---|---|
| `Bootstrap` | >= 5.3 (CDN) | Responsive CSS framework for dashboard layout and components. |
| `Chart.js` | >= 4.0 (CDN) | JavaScript charting library for attack stage distribution visualisation on the dashboard. |
| `Vanilla JavaScript` | ES2020+ | Client-side interactivity (filtering, sorting, polling for updates). |

### 6.3 Infrastructure and Tooling Dependencies

| Tool / Service | Version (approx.) | Purpose |
|---|---|---|
| `Docker` | >= 24.0 | Container runtime for all system components. |
| `Docker Compose` | >= 2.20 | Multi-container orchestration; defines and runs the full system. |
| `Ollama` | Latest stable | Local LLM inference server (serves the language model for lure generation). |
| `Python` | >= 3.10 | Runtime for all backend services and the attack simulator. |
| `SQLite` | >= 3.40 | Embedded relational database (included with Python stdlib via `sqlite3`). |

### 6.4 Development and Quality Tooling

| Tool | Purpose |
|---|---|
| `black` | Python code formatter (enforces consistent style). |
| `flake8` or `ruff` | Python linter (enforces PEP 8 compliance and catches common errors). |
| `mypy` | Static type checker for Python type annotations (NFR-04). |
| `git` | Version control. |

---

*End of Requirements Specification*

---

**Document Control:**

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0.0 | 2026-09-23 | Project Team | Initial baseline release. All requirements defined. |
