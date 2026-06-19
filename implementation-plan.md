 # Phase-Wise Implementation Plan: Weekly Product Review Pulse

This document outlines the step-by-step implementation strategy for the Weekly Product Review Pulse system (specifically tailored for the **Groww** platform on the **Google Play Store**). The project is divided into five logical phases to ensure modular development and incremental value delivery.

---

## Phase 1: Foundation & Data Ingestion
**Goal:** Establish the project foundation and reliably extract raw reviews from the Google Play Store.

- **1.1 Repository Setup:** Initialize the core agent repository and set up code quality tools, environment variables, and configuration management.
- **1.2 Scraper Implementation:** Build or integrate a Google Play Store scraper to fetch public reviews specifically for the Groww app.
- **1.3 Timeframe Filtering:** Implement logic to filter reviews based on the target ISO week or a sliding 8–12 week window.
- **1.4 Pagination & Rate Limiting:** Ensure the scraper robustly handles pagination and API rate limits to capture the full dataset without failure.
- **1.5 Local Data Storage:** Store raw scraped data locally (or in an intermediate database) to avoid repeated scraping during the development of downstream phases.

## Phase 2: Data Processing & Reasoning
**Goal:** Clean the data, identify patterns, and use an LLM to generate actionable insights.

- **2.1 PII Scrubbing:** Implement the data sanitization module to strip out any Personally Identifiable Information (PII) before it leaves the local environment.
- **2.2 Vectorization:** Convert the cleaned review texts into numerical embeddings.
- **2.3 Clustering (UMAP + HDBSCAN):** Apply dimensionality reduction (UMAP) and density-based clustering (HDBSCAN) to group similar customer feedback into distinct themes.
- **2.4 LLM Integration:**
  - Prompt the LLM to analyze each cluster and assign a descriptive theme name.
  - Instruct the LLM to propose "actionable ideas" based on the feedback.
- **2.5 Verbatim Quote Extraction & Validation:** Implement strict programmatic validation to ensure that any quote extracted by the LLM exists verbatim in the original source data (preventing hallucinations).

## Phase 3: Content & Output Generation
**Goal:** Transform the raw LLM output into the final, human-readable narrative.

- **3.1 Narrative Formatting:** Build the templating engine to render the insights into a cohesive one-page report containing:
  - Top Themes
  - Verbatim Quotes
  - Actionable Ideas
  - "Who this helps" section
- **3.2 Payload Preparation:** Format the report into Markdown/JSON for Google Docs and HTML/Plain Text for Gmail.

## Phase 4: MCP Servers & Delivery Integration
**Goal:** Connect the core agent to the external world using the Model Context Protocol (MCP).

- **4.1 Unified MCP Server Integration:**
  - Establish connection to the hosted Google MCP Server at `web-production-c2c29.up.railway.app`.
- **4.2 Google Docs Delivery:**
  - Implement the logic to append the newly generated weekly report (plain text) as a dated section to the running Groww system-of-record document using the MCP server.
- **4.3 Gmail Delivery:**
  - Format a concise stakeholder email that includes a deep link to the newly appended section in the Google Doc, and send it via the MCP server.
- **4.3 Credential Management:** Ensure that all Google OAuth secrets remain inside the MCP server configurations and are not exposed in the agent's codebase.

## Phase 5: Orchestration, Auditing & Deployment
**Goal:** Automate the pipeline, ensure safety/idempotency, and deploy to production.

- **5.1 Idempotency Mechanisms:**
  - Implement a stable section anchor check via the Docs MCP to prevent duplicate reports for the same ISO week.
  - Implement a run-scoped hash check (product + week) to prevent duplicate emails.
- **5.2 Audit Logging:** Record timestamps, token usage/costs, ISO weeks processed, and delivery identifiers (doc anchors, message IDs) for every run.
- **5.3 Cron Scheduling & CLI:** 
  - Set up the weekly automated trigger (e.g., Monday morning IST).
  - Build a CLI utility to allow manual triggering and historical backfilling of specific ISO weeks.
- **5.4 Final Testing & Cost Controls:** Perform end-to-end testing, verify token limit enforcement, and finalize production deployment.
