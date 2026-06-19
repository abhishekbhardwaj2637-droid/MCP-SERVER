import json
import os
from datetime import datetime
from pathlib import Path

def save_reviews_to_json(reviews: list[dict], output_dir: Path, app_package: str, suffix: str = "") -> str:
    """
    Saves a list of review dictionaries to a JSON file.
    Automatically generates a filename based on the app package, suffix, and current date.
    """
    date_str = datetime.now().strftime("%Y_%m_%d")
    filename = f"{app_package}_reviews{suffix}_{date_str}.json"
    filepath = output_dir / filename
    
    # We need to convert datetime objects to strings before serializing to JSON
    def default_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4, default=default_serializer)
        
    return str(filepath)
