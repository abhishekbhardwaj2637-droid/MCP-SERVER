from google_play_scraper import Sort, reviews
from datetime import datetime

def fetch_recent_reviews(app_id: str, lang: str = 'en', country: str = 'in', max_reviews: int = 5000) -> list[dict]:
    """
    Fetches the most recent reviews for a given app ID from the Google Play Store.
    Note: google-play-scraper does not natively support fetching by date bounds directly in a single call,
    so we fetch a large batch sorted by NEWEST and filter them down later.
    """
    print(f"Fetching up to {max_reviews} newest reviews for {app_id}...")
    
    result, continuation_token = reviews(
        app_id,
        lang=lang,
        country=country,
        sort=Sort.NEWEST,
        count=max_reviews
    )
    
    print(f"Fetched {len(result)} reviews.")
    return result
