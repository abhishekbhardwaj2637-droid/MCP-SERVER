import sys
from src.config import (
    APP_PACKAGE_NAME, 
    REVIEW_TIME_WINDOW_WEEKS, 
    MAX_REVIEWS_TO_FETCH,
    RAW_DATA_DIR,
    SCRAPER_LANG,
    SCRAPER_COUNTRY
)
from src.ingestion.play_store import fetch_recent_reviews
from src.ingestion.utils import filter_reviews_by_date, normalize_reviews
from src.storage.local_storage import save_reviews_to_json
import json
import argparse
from pathlib import Path
from datetime import datetime
import traceback
import os

# Phase 2 Imports
from src.reasoning.pii_scrubber import scrub_reviews
from src.reasoning.embedder import generate_embeddings
from src.reasoning.clusterer import cluster_reviews, group_reviews_by_cluster
from src.reasoning.llm_summarizer import process_all_clusters
from src.generation.templater import generate_reports
from src.delivery.mcp_client import deliver_to_docs, deliver_to_gmail
from src.orchestration.state_manager import is_week_processed, mark_week_processed
from src.orchestration.logger import log_info, log_error, log_success, log_audit

def run_phase_1():
    print(f"--- Starting Phase 1: Ingestion for {APP_PACKAGE_NAME} ---")
    
    # 1. Fetch reviews from Play Store
    all_reviews = fetch_recent_reviews(
        app_id=APP_PACKAGE_NAME,
        lang=SCRAPER_LANG,
        country=SCRAPER_COUNTRY,
        max_reviews=MAX_REVIEWS_TO_FETCH
    )
    
    if not all_reviews:
        print("No reviews fetched. Exiting.")
        sys.exit(0)
        
    # 2. Filter by timeframe
    print(f"Filtering reviews from the last {REVIEW_TIME_WINDOW_WEEKS} weeks...")
    filtered_reviews = filter_reviews_by_date(all_reviews, REVIEW_TIME_WINDOW_WEEKS)
    
    print(f"Remaining reviews after time filter: {len(filtered_reviews)}")
    
    if not filtered_reviews:
        print("No reviews within the specified timeframe. Exiting.")
        sys.exit(0)
        
    # 3. Save raw (filtered) to local storage
    print("Saving raw (filtered) reviews to local storage...")
    raw_filepath = save_reviews_to_json(filtered_reviews, RAW_DATA_DIR, f"{APP_PACKAGE_NAME}_raw")
    print(f"Raw data saved successfully at: {raw_filepath}")

    # 4. Normalize reviews
    print("Normalizing reviews (removing short, non-English, or emoji-containing reviews)...")
    normalized_reviews = normalize_reviews(filtered_reviews)
    
    print(f"Remaining reviews after normalization: {len(normalized_reviews)}")
    
    if not normalized_reviews:
        print("No reviews left after normalization. Exiting.")
        sys.exit(0)
        
    # 5. Save normalized to local storage
    print("Saving normalized reviews to local storage...")
    norm_filepath = save_reviews_to_json(normalized_reviews, RAW_DATA_DIR, f"{APP_PACKAGE_NAME}_normalized")
    
    print(f"Phase 1 Complete! Normalized data saved successfully at: {norm_filepath}")
    return normalized_reviews

def run_phase_2(reviews: list[dict]):
    print(f"\n--- Starting Phase 2: Processing & Reasoning ---")
    
    # 1. PII Scrubbing
    print("Scrubbing PII from reviews...")
    scrubbed_reviews = scrub_reviews(reviews)
    
    # 2. Vectorization (Embeddings)
    _, embeddings = generate_embeddings(scrubbed_reviews)
    
    # 3. Clustering
    labels = cluster_reviews(embeddings)
    clustered_data = group_reviews_by_cluster(scrubbed_reviews, labels)
    
    # 4. LLM Summarization
    report = process_all_clusters(clustered_data)
    
    # 5. Save Report
    PROCESSED_DATA_DIR = RAW_DATA_DIR.parent / "processed"
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    from datetime import datetime
    date_str = datetime.now().strftime("%Y_%m_%d")
    # Save JSON Report
    report_filename = f"com.nextbillion.groww_insights_{date_str}.json"
    report_path = save_reviews_to_json([report], PROCESSED_DATA_DIR, report_filename)
    print(f"Phase 2 Complete! Insights saved to: {report_path}\n")
    return report_path

def run_phase_3(insights_path: str):
    print("--- Starting Phase 3: Content & Output Generation ---")
    reports = generate_reports(insights_path)
    print("Phase 3 Complete!\n")
    return reports

def run_phase_4(reports: dict):
    print("--- Starting Phase 4: Delivery Integration (MCP) ---")
    
    # 1. Google Docs Delivery
    text_path = reports.get("text_path")
    if text_path and os.path.exists(text_path):
        with open(text_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
            deliver_to_docs(text_content)
            
    # 2. Gmail Delivery
    html_path = reports.get("html_path")
    if html_path and os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            deliver_to_gmail(html_content)
            
    print("Phase 4 Complete!\n")

def run_pipeline(target_week: str, force: bool):
    log_info(f"Starting pipeline for target week: {target_week}")

    if not force and is_week_processed(target_week):
        log_info(f"Week {target_week} has already been successfully processed. Skipping run. Use --force to override.")
        return

    try:
        # --- PHASE 1 ---
        log_info("Executing Phase 1: Ingestion & Normalization")
        normalized_reviews = run_phase_1()
        
        if not normalized_reviews:
            log_info("No reviews available after Phase 1. Exiting gracefully.")
            return

        # --- PHASE 2 ---
        log_info("Executing Phase 2: Processing & Reasoning")
        insights_path = run_phase_2(normalized_reviews)
        
        if not insights_path:
            log_error("Phase 2 failed to generate insights.")
            return

        # --- PHASE 3 ---
        log_info("Executing Phase 3: Content & Output Generation")
        reports = run_phase_3(insights_path)
        
        if not reports:
            log_error("Phase 3 failed to generate reports.")
            return

        # --- PHASE 4 ---
        log_info("Executing Phase 4: Delivery Integration (MCP)")
        run_phase_4(reports)
        
        # Mark as processed if everything succeeded
        mark_week_processed(target_week)
        log_success(f"Pipeline completed successfully for week {target_week}!")
        
        # --- PHASE 5 ---
        # Audit Logging
        audit_data = {
            "timestamp": datetime.now().isoformat(),
            "iso_week": target_week,
            "product": APP_PACKAGE_NAME,
            "doc_anchor": f"Week {target_week}",
            "status": "success",
            "token_usage": "N/A" # To be implemented
        }
        log_audit(audit_data)

    except Exception as e:
        log_error(f"Pipeline failed: {str(e)}")
        log_error(traceback.format_exc())

def main():
    parser = argparse.ArgumentParser(description="Weekly Product Review Pulse - Groww")
    parser.add_argument("--week", type=str, help="ISO week string to process, e.g., '2026-W22'. Defaults to current week.")
    parser.add_argument("--weeks", type=str, help="Comma-separated list of ISO week strings for backfilling, e.g., '2026-W20,2026-W21'")
    parser.add_argument("--force", action="store_true", help="Force run even if week is already processed.")
    args = parser.parse_args()

    weeks_to_process = []
    
    if args.weeks:
        weeks_to_process = [w.strip() for w in args.weeks.split(',')]
    elif args.week:
        weeks_to_process = [args.week.strip()]
    else:
        # Default to current week
        current_date = datetime.now()
        iso_year, iso_week, _ = current_date.isocalendar()
        weeks_to_process = [f"{iso_year}-W{iso_week:02d}"]

    for target_week in weeks_to_process:
        run_pipeline(target_week, args.force)



if __name__ == "__main__":
    main()
