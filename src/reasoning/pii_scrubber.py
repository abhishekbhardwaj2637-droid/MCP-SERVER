from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

class PIIScrubber:
    def __init__(self):
        print("Initializing PII Scrubber (Presidio)...")
        # Load the default NLP engine (spaCy)
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def scrub(self, text: str) -> str:
        if not text:
            return text
            
        # Analyze text for PII (names, emails, phone numbers, etc.)
        results = self.analyzer.analyze(
            text=text,
            language='en',
            entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "CREDIT_CARD", "CRYPTO"]
        )
        
        # Anonymize the found PII entities by replacing them with <ENTITY_TYPE>
        anonymized_result = self.anonymizer.anonymize(text=text, analyzer_results=results)
        return anonymized_result.text

def scrub_reviews(reviews: list[dict]) -> list[dict]:
    """
    Takes a list of normalized reviews and applies PII scrubbing to their content.
    """
    scrubber = PIIScrubber()
    scrubbed_reviews = []
    
    for review in reviews:
        content = review.get("content", "")
        clean_content = scrubber.scrub(content)
        
        scrubbed_review = review.copy()
        scrubbed_review["content"] = clean_content
        scrubbed_reviews.append(scrubbed_review)
        
    return scrubbed_reviews
