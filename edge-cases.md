# Edge Cases & Corner Cases: Weekly Product Review Pulse

This document outlines potential edge cases and corner cases that the system must handle to ensure robust, idempotent, and accurate execution for the Groww platform review pulse.

---

## 1. Data Retrieval (Ingestion Layer)

### 1.1 Play Store Scraper Failures
- **DOM Structure Changes:** Google Play Store updates its HTML structure, breaking the scraper.
  - *Mitigation:* Implement robust error handling, alerts on zero-record fetches, and consider using an official/unofficial API fallback if the scraper fails.
- **Rate Limiting & IP Bans:** Scraping too many reviews triggers Google's anti-bot protections.
  - *Mitigation:* Implement exponential backoff, randomized delays between page requests, and potentially proxy rotation if necessary.

### 1.2 Data Volume Anomalies
- **Zero Reviews Found:** The app receives no reviews within the configured 8-12 week window.
  - *Mitigation:* The system should gracefully halt, log the absence of data, and optionally send an email stating "No new reviews found" rather than failing.
- **Review Spikes (e.g., Post-Release Bug):** An update causes thousands of negative reviews, leading to out-of-memory (OOM) errors during clustering.
  - *Mitigation:* Implement strict limits on the number of reviews processed (e.g., cap at 5,000 most recent/relevant) to protect memory and LLM context limits.

### 1.3 Data Quality Issues
- **Non-English Reviews:** Users leave reviews in Hindi, Hinglish, or other languages.
  - *Mitigation:* Add a language detection filter to only process English, or ensure the LLM/Embedding model is explicitly instructed and capable of multilingual processing.

---

## 2. Processing & Reasoning (Clustering + LLM Layer)

### 2.1 Context Window & Token Limit Breaches
- **Oversized Payloads:** The combined review text for a cluster exceeds the LLM's maximum context window.
  - *Mitigation:* Implement chunking strategies or summarize sub-clusters before doing a final aggregation. Enforce strict token limits per run.

### 2.2 Hallucinations & Quote Mismatches
- **Fabricated Verbatim Quotes:** The LLM "hallucinates" a quote that sounds realistic but doesn't exist in the raw data.
  - *Mitigation:* The strict programmatic validation step must cross-reference every LLM-generated quote against the raw dataset (using exact substring matching). If a quote fails validation, it is stripped or the LLM is reprompted.

### 2.3 Clustering Anomalies
- **The "Everything is One Theme" Problem:** HDBSCAN groups 90% of reviews into a single massive cluster due to vague embeddings.
  - *Mitigation:* Tune UMAP/HDBSCAN hyperparameters dynamically based on review volume, or run a recursive clustering step for oversized clusters.

### 2.4 PII Scrubbing Failures
- **Obfuscated PII:** Users enter phone numbers with spaces (e.g., "9 8 7 6...") or emails in non-standard formats which bypass basic regex scrubbers.
  - *Mitigation:* Use an advanced NLP-based PII scrubber (e.g., Presidio) rather than relying solely on Regex.

---

## 3. Rendering & Output Layer

### 3.1 Content Truncation
- **Extremely Long Reports:** The generated narrative is too large and breaks formatting expectations or Docs/Gmail payload limits.
  - *Mitigation:* Enforce maximum lengths for the "Action Ideas" and "Quotes" sections in the LLM prompt.

---

## 4. Delivery & MCP Integration

### 4.1 Idempotency Failures
- **Deleted Anchors:** A human stakeholder accidentally deletes the hidden anchor or previous heading in the Google Doc, causing the system to think a run hasn't happened.
  - *Mitigation:* Store run history locally (or in a lightweight DB/metadata file) as a secondary idempotency check alongside the Doc anchor.
- **Race Conditions:** Two cron jobs run simultaneously for the same ISO week.
  - *Mitigation:* Implement a run lock mechanism.

### 4.2 MCP Server Outages
- **Server Unreachable:** The Google Docs or Gmail MCP server is down or unreachable during the delivery phase.
  - *Mitigation:* Implement a retry queue. If delivery fails, the agent should save the generated payload locally and alert admins, allowing for a manual retry without re-running the expensive LLM steps.

### 4.3 Google Ecosystem Limits
- **Docs Size Limits:** The master running Google Doc eventually hits Google Docs' maximum file size or character limit after years of weekly pulses.
  - *Mitigation:* Implement automatic document rotation (e.g., "Groww Review Pulse - 2026", "Groww Review Pulse - 2027") once a certain size or date threshold is reached.
