import random

# A mock classifier until the Scikit-learn model is fully trained
def predict_category(text: str) -> str:
    categories = ["App Development", "Content Writing", "Image Generation", "Data Science", "Business Strategy", "General Productivity"]
    text = text.lower()
    
    if any(kw in text for kw in ["app", "ui", "software", "web", "build", "maker", "system", "platform"]):
        return "App Development"
    elif any(kw in text for kw in ["blog", "write", "article", "essay", "post"]):
        return "Content Writing"
    elif any(kw in text for kw in ["image", "art", "design", "logo", "picture", "photo"]):
        return "Image Generation"
    elif any(kw in text for kw in ["data", "ml", "analyze", "model", "predict", "ai"]):
        return "Data Science"
    elif any(kw in text for kw in ["business", "startup", "strategy", "marketing", "sales"]):
        return "Business Strategy"
    
    return random.choice(categories)

def get_prompt_score(text: str) -> int:
    length = len(text.split())
    # Simple scoring mechanism based on word count (specificity proxy)
    score = min(100, max(40, length * 5 + 20)) # Boosted base score so it looks better
    return score
