from datetime import datetime, timedelta
import emoji
from langdetect import detect, LangDetectException

def is_within_time_window(review_date: datetime, weeks_window: int) -> bool:
    """
    Checks if a given review_date is within the last `weeks_window` weeks.
    """
    cutoff_date = datetime.now() - timedelta(weeks=weeks_window)
    return review_date >= cutoff_date

def filter_reviews_by_date(reviews: list[dict], weeks_window: int) -> list[dict]:
    """
    Filters a list of review dictionaries, keeping only those within the timeframe.
    Expects 'at' key in the review dictionary to be a datetime object.
    """
    filtered = []
    for review in reviews:
        review_date = review.get("at")
        if review_date and is_within_time_window(review_date, weeks_window):
            filtered.append(review)
    return filtered

def normalize_reviews(reviews: list[dict]) -> list[dict]:
    """
    Normalizes a list of reviews:
    1. Removes reviews with fewer than 8 words.
    2. Removes reviews containing emojis.
    3. Removes reviews that are not in English.
    """
    normalized = []
    for review in reviews:
        content = review.get("content", "")
        if not content:
            continue
            
        # 1. Check word count
        words = content.split()
        if len(words) < 8:
            continue
            
        # 2. Check for emojis
        if emoji.emoji_count(content) > 0:
            continue
            
        # 3. Check language
        try:
            lang = detect(content)
            if lang != 'en':
                continue
        except LangDetectException:
            # If language cannot be detected, we discard it
            continue
            
        # Strip out unnecessary metadata
        clean_review = {
            "content": content,
            "score": review.get("score"),
            "at": review.get("at"),
            "thumbsUpCount": review.get("thumbsUpCount")
        }
            
        normalized.append(clean_review)
        
    return normalized
