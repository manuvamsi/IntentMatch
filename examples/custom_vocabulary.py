"""
Custom vocabulary example for the Intent Identity Framework.

This example shows how to extend the framework with custom intent tags.
"""

import json
from pathlib import Path
from iif import SimilarityScorer


def add_custom_tag():
    """Add a custom intent tag to the vocabulary."""
    
    # Path to intent tags vocabulary
    vocab_path = Path(__file__).parent.parent / "vocabularies" / "intent_tags.json"
    
    # Load existing tags
    with open(vocab_path, 'r') as f:
        tags = json.load(f)
    
    # Add a new custom tag
    tags["medical_advice"] = {
        "description": "Provides medical or health-related guidance",
        "rules": {
            "required": ["goal"],
            "keywords": ["medical", "health", "symptom", "diagnosis", "treatment", "doctor"]
        },
        "parent": None
    }
    
    # Save updated vocabulary
    with open(vocab_path, 'w') as f:
        json.dump(tags, f, indent=2)
    
    print("Added custom tag 'medical_advice' to vocabulary!")


def test_custom_tag():
    """Test the custom tag."""
    
    scorer = SimilarityScorer()
    
    prompt1 = """
    You are a medical AI assistant. Provide health advice based on symptoms.
    Always recommend consulting a doctor for serious conditions.
    """
    
    prompt2 = """
    Act as a health advisor. Give medical guidance for common symptoms.
    Remind users to see a doctor when necessary.
    """
    
    result = scorer.compare(prompt1, prompt2)
    
    print("\nTesting custom tag:")
    print(f"Similarity Score: {result['similarity_score']}")
    print(f"Matched Tags: {result['explanation']['matched_tags']}")
    print(f"Tags for Prompt 1: {result['details']['tags1']['primary_tags']}")
    print(f"Tags for Prompt 2: {result['details']['tags2']['primary_tags']}")


def main():
    print("=" * 60)
    print("Custom Vocabulary Example")
    print("=" * 60)
    
    # Add custom tag
    add_custom_tag()
    
    # Test it
    test_custom_tag()
    
    print("\n" + "=" * 60)
    print("Custom tag successfully integrated!")
    print("The framework now recognizes medical advice prompts.")
    print("=" * 60)


if __name__ == "__main__":
    main()
