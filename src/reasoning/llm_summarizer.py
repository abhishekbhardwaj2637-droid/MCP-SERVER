import os
import json
from google import genai
from google.genai import types
from typing import Optional
from dotenv import load_dotenv

def setup_gemini():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("WARNING: GEMINI_API_KEY not found in environment. LLM summarization will fail.")
        return False
    return True

def generate_cluster_insights(reviews: list[dict], model_name: str = 'gemini-2.5-flash') -> Optional[dict]:
    """
    Takes a list of reviews belonging to a single cluster and asks Gemini to:
    1. Name the theme.
    2. Extract verbatim quotes.
    3. Propose actionable ideas.
    Returns a dictionary of the insights.
    """
    if not setup_gemini():
        return None
        
    # We only take up to 50 reviews from the cluster to avoid massive context window overload,
    # though Gemini 1.5 has a huge context window, it's better to keep it concise for the prompt.
    sampled_reviews = reviews[:50]
    
    # Build the prompt payload
    reviews_text = "\n".join([f"- {r.get('content')}" for r in sampled_reviews])
    
    prompt = f"""
    You are an expert product manager analyzing app reviews for a fintech platform.
    Below is a cluster of reviews that share a common theme.
    
    Reviews:
    {reviews_text}
    
    Task:
    Analyze the reviews and output a JSON object with the following schema:
    {{
        "theme_name": "A concise, 3-5 word name for the primary issue or theme in this cluster.",
        "quotes": [
            "Exact verbatim quote 1 from the reviews above that perfectly illustrates the theme",
            "Exact verbatim quote 2 from the reviews above"
        ],
        "action_ideas": [
            "Actionable product/engineering idea 1 to address this theme",
            "Actionable idea 2"
        ]
    }}
    
    CRITICAL RULE FOR QUOTES: You MUST extract the quotes EXACTLY word-for-word as they appear in the provided reviews. Do not modify, summarize, or hallucinate the quotes.
    
    Return ONLY valid JSON. Do not wrap it in markdown block quotes (```json ... ```).
    """
    
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        # Parse the JSON response
        insights = json.loads(response.text)
        
        # Programmatic Validation: Ensure quotes actually exist in the raw text
        validated_quotes = []
        raw_texts = [r.get('content', '') for r in reviews] # check against all reviews in cluster
        for quote in insights.get('quotes', []):
            # Check if quote exists as a substring in any of the raw reviews
            if any(quote in text for text in raw_texts):
                validated_quotes.append(quote)
            else:
                print(f"Validation Warning: Hallucinated or modified quote stripped: '{quote}'")
                
        insights['quotes'] = validated_quotes
        return insights
        
    except Exception as e:
        print(f"Error communicating with Gemini or parsing JSON: {e}")
        return None

def process_all_clusters(clustered_data: dict[int, list[dict]]) -> dict:
    """
    Iterates through all discovered clusters, generates insights for each,
    and returns a combined report structure.
    """
    report = {
        "clusters": []
    }
    
    print(f"Generating LLM insights for {len(clustered_data)} clusters...")
    
    import time
    
    for cluster_id, reviews in clustered_data.items():
        print(f"Processing Cluster {cluster_id} (Size: {len(reviews)} reviews)...")
        insights = generate_cluster_insights(reviews)
        
        if insights:
            insights['cluster_id'] = cluster_id
            insights['review_count'] = len(reviews)
            report['clusters'].append(insights)
            
        print("Sleeping 15 seconds to respect Gemini API free tier rate limits (5 requests/minute)...")
        time.sleep(15)
            
    # Sort clusters by review count (descending) so biggest issues are on top
    report['clusters'] = sorted(report['clusters'], key=lambda x: x['review_count'], reverse=True)
    return report
