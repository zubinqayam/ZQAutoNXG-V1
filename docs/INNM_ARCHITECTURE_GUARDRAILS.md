# INNM Architecture Guardrails

> **Platform:** ZQAutoNXG — Powered by ZQ AI LOGIC™  
> **Scope:** INNM pipeline — Notion/BI source → change detection → normalization/WOSDS → validation/Meaning Engine → intelligence/PowerBox → append-only ledger → snapshots/patterns/monitoring  
> **Status:** Authoritative reference — all pipeline implementations must comply.

---

## 1. Pipeline Overview

```
Notion / BI Source
       │
       ▼
Change Detection (per-source cursors, last_edited_time)
       │
       ▼
Normalization / WOSDS (Workspace-Oriented Semantic Data Schema)
       │
       ▼
Validation / Meaning Engine (schema, semantic, PII redaction)
       │
       ▼
Intelligence / PowerBox (AI enrichment, workspace-scoped)
       │
       ▼
Append-Only Ledger (immutable, hash-chained)
       │
       ▼
Snapshots / Patterns / Monitoring
```

Each stage must be idempotent, workspace-isolated, and fully auditable.

---

## 2. Notion Monitoring Reality

### 2.1 No Universal Change Feed
Notion does not provide a universal `get_recent_changes` API across all databases and pages. Implementations must **not** assume such an API exists.

### 2.2 Required Approach
- **Database/page discovery:** Enumerate databases and pages via `POST /v1/databases/{id}/query` and `GET /v1/pages/{id}`, filtering by `last_edited_time >= cursor_timestamp`.
- **Per-source cursors:** Each monitored Notion database or page collection maintains its own `last_polled_at` cursor persisted in the pipeline state store. On each poll cycle, only entries with `last_edited_time > cursor` are fetched.
- **Webhooks (where available):** Notion's webhook API (when enabled for a workspace) may supplement polling but must never be the sole mechanism — polling provides durability guarantees.
- **Cursor durability:** Cursors must be committed atomically with the ledger entry for the corresponding batch to prevent re-processing or missed entries on restart.

### 2.3 Rate Limiting
Notion API calls must respect rate limits (3 requests/second per integration as of current limits). Implement exponential backoff with jitter on `429 Too Many Requests` and `5xx` responses.

---

## 3. Duplicate Processing Prevention — Idempotency Keys

Every ingested entry must carry an idempotency key composed of:

```
idempotency_key = sha256(workspace_id + ":" + entry_id + ":" + last_edited_time_iso)
```

If `last_edited_time` is unavailable (e.g., BI sources), substitute with a deterministic content hash:

```
idempotency_key = sha256(workspace_id + ":" + entry_id + ":" + sha256(canonical_content))
```

### 3.1 Deduplication Check
Before any write operation (normalization, ledger append, vector index upsert), the pipeline must:
1. Look up `idempotency_key` in the idempotency store (e.g., a keyed Redis SET or a dedicated DB table with a unique constraint).
2. If already present: skip processing and emit a `duplicate_skipped` metric.
3. If absent: proceed with processing, then atomically record the key.

### 3.2 Key Expiry
Idempotency keys may be expired after the retention window (default: 30 days) to bound storage growth. Adjust per compliance requirements.

---

## 4. Failure Handling

### 4.1 Retry Policy
All external calls (Notion API, BI APIs, AI providers, databases) must implement:

| Attempt | Delay         | Max delay |
|---------|---------------|-----------|
| 1       | 1 s           | —         |
| 2       | 2 s           | —         |
| 3       | 4 s           | —         |
| 4       | 8 s           | —         |
| N       | min(2^N s, 60 s) + jitter | 60 s |

Retry only on transient errors (`429`, `500`, `502`, `503`, `504`, network timeouts). Do **not** retry on `4xx` client errors (except `429`).

### 4.2 Dead-Letter Queue
After exhausting retries, the failed item must be placed on a **dead-letter queue (DLQ)**. The DLQ entry must include:

- Original payload (redacted of any raw PII — see §6).
- Error details (type, message, HTTP status if applicable).
- Attempt count and timestamps.
- `idempotency_key` for deduplication on reprocessing.
- `workspace_id` and `entry_id` for traceability.

### 4.3 Human-Review Quarantine
DLQ items that cannot be automatically reprocessed after a configurable threshold (default: 3 replay attempts) must be routed to a **human-review quarantine queue**, not silently discarded or auto-corrected. The quarantine record must include all DLQ fields plus a `requires_human_review: true` flag.

**Silent auto-correction is prohibited** — see §5.

---

## 5. Self-Healing Rules

### 5.1 No Silent Overwrite
The pipeline must **never** silently overwrite source data. Any proposed correction (normalization adjustment, deduplication resolution, schema coercion) must be recorded as a **proposed correction record** with the following fields:

| Field              | Description                                              |
|--------------------|----------------------------------------------------------|
| `correction_id`    | UUID for this proposal                                   |
| `idempotency_key`  | Key of the affected entry                                |
| `original_value`   | The original value (redacted if PII)                     |
| `proposed_value`   | The corrected value                                      |
| `confidence_score` | Float 0.0–1.0 indicating automated confidence            |
| `rationale`        | Human-readable explanation of why the correction is proposed |
| `model_version`    | Version of the AI/rule model that generated this proposal |
| `approval_status`  | `pending` \| `approved` \| `rejected`                   |
| `created_at`       | UTC ISO 8601 timestamp                                   |
| `approved_by`      | User/system that approved or rejected (null if pending)  |

Corrections with `confidence_score >= 0.95` and no PII involvement may be auto-applied after a configurable grace period, provided an audit trail is maintained.  All others require explicit human approval.

---

## 6. Privacy — Raw Content Must Never Be Stored

The principle "raw content never stored" applies comprehensively:

### 6.1 Covered Surfaces
The following surfaces must **never** contain raw (unredacted) source content:

- Application logs (stdout, stderr, structured log sinks).
- AI prompts sent to any external provider.
- Exception traces and error messages.
- Snapshots and materialized views.
- Vector index documents and metadata.
- Audit records (store identifiers and hashes, not content).
- DLQ and quarantine queue payloads.

### 6.2 Redaction Before AI Processing
Before any content is sent to an AI provider (including the INNM pipeline's own Meaning Engine or PowerBox):
1. Apply PII detection (names, emails, phone numbers, national IDs, health data, financial data).
2. Replace detected PII with typed placeholders: `[PERSON_NAME]`, `[EMAIL]`, `[PHONE]`, `[HEALTH_DATA]`, etc.
3. Apply the secret redaction pass (see §3 of the AI Quality Gate script).
4. Log the redaction summary (counts by type) but never the original values.

### 6.3 Minimization
Ingest only the fields required for downstream processing. Do not cache or persist fields not needed for the current pipeline stage.

---

## 7. Cross-Workspace Learning Restrictions

AI enrichment, embedding generation, retrieval-augmented generation (RAG), and pattern learning must enforce strict workspace isolation:

- **Embeddings:** Each workspace's vector index is logically (and preferably physically) isolated. No cross-workspace similarity search unless the user has explicitly authorized data sharing between specific workspaces.
- **Prompts:** Context injected into AI prompts must contain only data from the requesting workspace. Retrieval results must be filtered by `workspace_id` before injection.
- **Model fine-tuning/adaptation:** Workspace-specific fine-tuning data must not be mixed with another workspace's data without explicit bilateral authorization, recorded in the audit ledger.
- **Authorization record:** Any cross-workspace access must reference an `authorization_id` recorded in the ledger, with the authorizing workspace owners identified.

---

## 8. Ledger Integrity Requirements

The append-only ledger is the system of record for all pipeline events. Every ledger entry must contain:

| Field               | Type         | Description                                              |
|---------------------|--------------|----------------------------------------------------------|
| `sequence_number`   | uint64       | Monotonically increasing, per-workspace, never reused    |
| `previous_hash`     | hex string   | SHA-256 of the previous entry's canonical payload        |
| `payload_hash`      | hex string   | SHA-256 of this entry's canonical payload (before signing)|
| `signing_key_id`    | string       | Identifier of the key used to sign this entry            |
| `signing_key_version` | string     | Version of the signing key                               |
| `signature`         | base64 string| HMAC-SHA256 or asymmetric signature over the payload     |
| `workspace_id`      | string       | Tenant/workspace scope                                   |
| `event_type`        | string       | Enumerated event type (e.g., `entry_ingested`, `correction_proposed`) |
| `idempotency_key`   | string       | Links to the source entry                                |
| `created_at`        | ISO 8601 UTC | Timestamp of ledger append                               |
| `schema_version`    | string       | Version of the ledger entry schema                       |

### 8.1 Verification Jobs
A scheduled verification job must run at minimum every 24 hours and:
1. Walk the chain from the last verified checkpoint, recomputing `payload_hash` and `previous_hash` for each entry.
2. Verify the signature against the recorded `signing_key_id` and `signing_key_version`.
3. Emit a `ledger_verification_passed` or `ledger_verification_failed` metric (see §9).
4. On failure, page the on-call rotation and halt new ledger appends until the integrity issue is resolved.

---

## 9. Monitoring Metrics

All metrics must be exposed at `/metrics` in Prometheus format and collected by the observability stack.

| Metric name                              | Type      | Labels                        | Description                                              |
|------------------------------------------|-----------|-------------------------------|----------------------------------------------------------|
| `innm_ingestion_lag_seconds`             | Gauge     | `workspace_id`, `source`      | Time since the oldest unprocessed entry's `last_edited_time` |
| `innm_ingestion_failures_total`          | Counter   | `workspace_id`, `source`, `error_type` | Total ingestion failures                        |
| `innm_duplicates_skipped_total`          | Counter   | `workspace_id`, `source`      | Entries skipped due to idempotency key match             |
| `innm_quarantine_queue_depth`            | Gauge     | `workspace_id`                | Number of items currently in human-review quarantine     |
| `innm_schema_drift_events_total`         | Counter   | `workspace_id`, `source`      | Schema validation failures indicating source drift       |
| `innm_ai_cost_usd_total`                 | Counter   | `workspace_id`, `model`       | Cumulative AI provider cost in USD                       |
| `innm_ai_false_positive_reviews_total`   | Counter   | `workspace_id`                | AI review findings later marked as false positives       |
| `innm_ai_false_negative_reviews_total`   | Counter   | `workspace_id`                | Issues missed by AI review and found in post-review audit|
| `innm_ledger_verification_passed_total`  | Counter   | `workspace_id`                | Successful ledger integrity verification runs            |
| `innm_ledger_verification_failed_total`  | Counter   | `workspace_id`                | Failed ledger integrity verification runs                |
| `innm_retry_attempts_total`              | Counter   | `workspace_id`, `source`, `attempt` | Total retry attempts by attempt number             |
| `innm_correction_proposals_total`        | Counter   | `workspace_id`, `status`      | Correction proposals by approval status                  |

---

## 10. Compliance and Audit Summary

- All pipeline stages are covered by the append-only ledger (§8).
- PII is redacted before storage or AI processing (§6).
- Cross-workspace data access requires explicit authorization recorded in the ledger (§7).
- Human review is mandatory for quarantined items (§4.3) and uncertain corrections (§5).
- Monitoring metrics provide full operational visibility (§9).
- Ledger integrity is verified on a scheduled basis (§8.1).

---

*Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™. Licensed under the Apache License 2.0.*
