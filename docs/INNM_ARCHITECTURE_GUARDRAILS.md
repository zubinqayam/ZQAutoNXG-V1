# INNM Universal Intelligence System — Architecture Guardrails

This document closes the implementation gaps identified when designing the
INNM Universal Intelligence System (centralized hub architecture) and
records how they are enforced in `ZQAutoNXG-V1` via the AI Quality Gate.

## 1. Pipeline contract

```
Notion / BI source
   -> change detection (cursor / last_edited_time / webhook)
   -> WOSDS normalization (canonical structure + hash)
   -> Meaning Engine validation (tri-loop)
   -> PowerBox intelligence scoring
   -> append-only ledger write
   -> snapshots, pattern learning, monitoring
```

Every stage must be traceable by a single `entry_id` and `workspace_id` pair
end to end. Pull requests that skip a stage, or write to the ledger before
validation completes, are flagged `HIGH` by the AI Quality Gate.

## 2. Change detection

- The Notion API has no universal "get recent changes" call. Implementations
  must page through `databases.query` / `pages` search results filtered by
  `last_edited_time`, or subscribe to webhooks where available.
- Each workspace connector persists its own cursor (`last_polled_at` or
  webhook cursor) so restarts do not reprocess the entire workspace.

## 3. Idempotency

- Every ledger write is keyed by
  `workspace_id + entry_id + content_hash(last_edited_time)`.
- Duplicate keys are rejected at the storage layer, not just filtered in
  application code.

## 4. Failure handling

- Failed ingestion items retry with exponential backoff (max 5 attempts).
- Items exceeding retry limits move to a dead-letter/quarantine store for
  human review — never silently dropped or auto-corrected.
- Self-healing corrections are proposals: they are stored with confidence
  score, rationale, and approval status, and only applied to the canonical
  record after explicit approval.

## 5. Privacy boundaries

- Raw Notion/BI content must never be persisted in the ledger, logs,
  snapshots, AI prompts, exception traces, or vector indexes.
- Only canonical hashes, meaning-block IDs, and intelligence scores are
  stored centrally.
- Data sent to any AI reviewer or model is redacted of credentials before
  transmission (see `.github/scripts/run_ai_quality_gate.py`).

## 6. Workspace isolation

- Cross-workspace pattern learning operates on de-identified pattern
  vectors only, scoped by explicit tenant authorization — never on raw
  content, embeddings, or retrieval results mixed across workspaces
  without consent.

## 7. Ledger integrity

Each ledger entry requires:

- `sequence_number`
- `previous_hash`
- `canonical_payload_hash`
- `timestamp` (UTC, ISO 8601)
- `signing_key_version`

A scheduled verification job re-walks the hash chain and alerts on any
mismatch.

## 8. Monitoring

Track and alert on: ingestion lag, failure rate, duplicate-write rate,
quarantine queue depth, schema drift score, AI review cost, and AI
false-positive/false-negative rate (validated against human review
outcomes).

## 9. CI/CD enforcement

- `.github/workflows/ai-quality-gate.yml` runs on every pull request into
  `main`.
- It filters out generated/binary/lockfile noise before any AI call
  ("trash filtering") and only reviews changes relevant to tracked source
  paths ("branch filtering" of the diff scope).
- `CRITICAL` findings (e.g., exposed secrets, missing auth) block merge.
- `HIGH` findings require a resolution comment before merge.
- `MEDIUM`/`LOW` findings are advisory only.

## 10. Secrets policy

- Gemini API keys are stored only as GitHub Actions repository secrets
  (e.g. `GEMINI_API_KEY`), never in Notion, YAML, `.env.example`,
  or code.
- SSH **deploy keys** (Settings → Deploy keys) are for pulling code onto a
  deployment host only. They are unrelated to AI provider credentials and
  should not have write access unless a deployment process must push
  release artifacts back to the repository.
