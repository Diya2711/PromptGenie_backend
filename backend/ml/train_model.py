import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pickle
import os

# Dummy dataset
data = {
    "text": [
        "I want to build a flutter app for task management",
        "Write a blog post about AI in healthcare",
        "Generate a cyberpunk city illustration",
        "Train a model to predict house prices",
        "Create an e-commerce website using react",
        "Write an essay on climate change",
        "Design a logo for a coffee shop",
        "Analyze customer churn data using pandas"
    ],
    "label": [
        "App Development",
        "Content Writing",
        "Image Generation",
        "Data Science",
        "App Development",
        "Content Writing",
        "Image Generation",
        "Data Science"
    ]
}

def train_model():
    print("Training Intent Classification Model...")
    df = pd.DataFrame(data)
    
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(df["text"], df["label"])
    
    accuracy = model.score(df["text"], df["label"])
    print(f"Training Complete. Accuracy: {accuracy * 100:.2f}%")
    
    # Save the model
    os.makedirs("models_bin", exist_ok=True)
    with open("models_bin/intent_classifier.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Model saved to models_bin/intent_classifier.pkl")

if __name__ == "__main__":
    train_model()
