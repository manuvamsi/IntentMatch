"""
Basic usage example for the Intent Identity Framework.

This example shows how to compare two prompts for similarity.
"""

from iif import SimilarityScorer
import json


def main():
    # Initialize the scorer
    scorer = SimilarityScorer()
    
    # Example 1: Two similar roleplay prompts
    print("=" * 60)
    print("Example 1: Similar Roleplay Prompts")
    print("=" * 60)
    
    prompt1 = """
    You are Sheldon Cooper from The Big Bang Theory.
    You must always respond with scientific accuracy and use the catchphrase "Bazinga!" 
    when making jokes. Stay in character at all times.
    """
    
    prompt2 = """
    Act as Sheldon Cooper. You should maintain strict character consistency,
    always be scientifically precise, and never break character.
    Use "Bazinga!" as your signature phrase.
    """
    
    result = scorer.compare(prompt1, prompt2)
    
    print(f"\nSimilarity Score: {result['similarity_score']}")
    print(f"Verdict: {result['verdict']}")
    print(f"\nBreakdown:")
    print(f"  - Structural: {result['breakdown']['structural']}")
    print(f"  - Tag Overlap: {result['breakdown']['tag_overlap']}")
    print(f"  - Pattern Match: {result['breakdown']['pattern_match']}")
    
    print(f"\nMatched Tags: {result['explanation']['matched_tags']}")
    print(f"Key Similarities: {result['explanation']['key_similarities']}")
    
    # Example 2: Different prompts
    print("\n" + "=" * 60)
    print("Example 2: Different Prompts")
    print("=" * 60)
    
    prompt3 = """
    Write a creative story about a robot learning to feel emotions.
    Make it engaging and heartwarming.
    """
    
    prompt4 = """
    Extract all email addresses from the following text and format them as a JSON array.
    """
    
    result2 = scorer.compare(prompt3, prompt4)
    
    print(f"\nSimilarity Score: {result2['similarity_score']}")
    print(f"Verdict: {result2['verdict']}")
    print(f"\nKey Differences: {result2['explanation']['key_differences']}")
    
    # Example 3: Save detailed report
    print("\n" + "=" * 60)
    print("Example 3: Saving Detailed Report")
    print("=" * 60)
    
    with open("similarity_report.json", "w") as f:
        json.dump(result, f, indent=2)
    
    print("Detailed report saved to similarity_report.json")


if __name__ == "__main__":
    main()
