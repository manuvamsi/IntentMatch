"""
Standalone demo script for the Intent Identity Framework.
This script can run without installing the package.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from iif import SimilarityScorer
import json


def print_separator(title=""):
    """Print a visual separator."""
    if title:
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    else:
        print("=" * 60)


def demo_similar_prompts():
    """Demo 1: Similar roleplay prompts."""
    print_separator("Demo 1: Similar Roleplay Prompts")
    
    scorer = SimilarityScorer()
    
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
    
    print("\nPrompt 1:")
    print(prompt1.strip())
    print("\nPrompt 2:")
    print(prompt2.strip())
    
    result = scorer.compare(prompt1, prompt2)
    
    print(f"\n✓ Similarity Score: {result['similarity_score']}")
    print(f"✓ Verdict: {result['verdict'].replace('_', ' ').title()}")
    print(f"\nBreakdown:")
    print(f"  • Structural: {result['breakdown']['structural']:.3f}")
    print(f"  • Tag Overlap: {result['breakdown']['tag_overlap']:.3f}")
    print(f"  • Pattern Match: {result['breakdown']['pattern_match']:.3f}")
    
    print(f"\n✓ Matched Tags: {', '.join(result['explanation']['matched_tags'])}")
    if result['explanation']['key_similarities']:
        print(f"✓ Key Similarities:")
        for sim in result['explanation']['key_similarities']:
            print(f"  • {sim}")


def demo_different_prompts():
    """Demo 2: Different prompts."""
    print_separator("Demo 2: Different Prompts")
    
    scorer = SimilarityScorer()
    
    prompt1 = """
    Write a creative story about a robot learning to feel emotions.
    Make it engaging and heartwarming.
    """
    
    prompt2 = """
    Extract all email addresses from the following text and format them as a JSON array.
    """
    
    print("\nPrompt 1:")
    print(prompt1.strip())
    print("\nPrompt 2:")
    print(prompt2.strip())
    
    result = scorer.compare(prompt1, prompt2)
    
    print(f"\n✓ Similarity Score: {result['similarity_score']}")
    print(f"✓ Verdict: {result['verdict'].replace('_', ' ').title()}")
    
    if result['explanation']['key_differences']:
        print(f"\n✓ Key Differences:")
        for diff in result['explanation']['key_differences']:
            print(f"  • {diff}")


def demo_batch_processing():
    """Demo 3: Batch processing to find duplicates."""
    print_separator("Demo 3: Batch Duplicate Detection")
    
    scorer = SimilarityScorer()
    
    prompts = [
        "You are a helpful AI assistant. Answer questions clearly.",
        "Act as a helpful assistant. Provide clear answers.",
        "Write a poem about nature in the style of Robert Frost.",
        "Generate a nature poem inspired by Robert Frost.",
        "Extract all dates from text and format as YYYY-MM-DD.",
    ]
    
    print(f"\nAnalyzing {len(prompts)} prompts for duplicates...\n")
    
    duplicates_found = 0
    
    for i in range(len(prompts)):
        for j in range(i + 1, len(prompts)):
            result = scorer.compare(prompts[i], prompts[j])
            
            if result['similarity_score'] >= 0.65:
                duplicates_found += 1
                print(f"✓ Duplicate Found (Pair {i+1}-{j+1}): {result['similarity_score']:.3f}")
                print(f"  Prompt {i+1}: {prompts[i][:50]}...")
                print(f"  Prompt {j+1}: {prompts[j][:50]}...")
                print(f"  Tags: {', '.join(result['explanation']['matched_tags'])}")
                print()
    
    total_comparisons = len(prompts) * (len(prompts) - 1) // 2
    print(f"Summary:")
    print(f"  • Total prompts: {len(prompts)}")
    print(f"  • Comparisons made: {total_comparisons}")
    print(f"  • Duplicates found: {duplicates_found}")


def demo_explainability():
    """Demo 4: Explainability features."""
    print_separator("Demo 4: Explainability & Transparency")
    
    scorer = SimilarityScorer()
    
    prompt1 = "You are a teacher. Explain concepts clearly with examples."
    prompt2 = "Act as an educator. Use examples to explain ideas."
    
    print("\nComparing two prompts...")
    print(f"Prompt 1: {prompt1}")
    print(f"Prompt 2: {prompt2}")
    
    result = scorer.compare(prompt1, prompt2)
    
    print(f"\n✓ Overall Similarity: {result['similarity_score']:.3f}")
    print(f"\n✓ Detailed Breakdown:")
    print(f"  • Structural Similarity: {result['breakdown']['structural']:.3f}")
    print(f"  • Tag Overlap: {result['breakdown']['tag_overlap']:.3f}")
    print(f"  • Pattern Match: {result['breakdown']['pattern_match']:.3f}")
    
    print(f"\n✓ Explanation:")
    print(f"  • Matched Tags: {result['explanation']['matched_tags']}")
    print(f"  • Matched Patterns: {result['explanation']['matched_patterns']}")
    print(f"  • Structural Differences: {result['explanation']['structural_differences']}")
    
    print(f"\n✓ This demonstrates:")
    print(f"  • Every score is broken down into components")
    print(f"  • Clear reasoning for similarity/difference")
    print(f"  • No black-box AI decisions")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Intent Identity Framework (IIF) - Live Demo".center(58) + "║")
    print("║" + "  Deterministic, Explainable Duplicate Detection".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    try:
        demo_similar_prompts()
        demo_different_prompts()
        demo_batch_processing()
        demo_explainability()
        
        print_separator("Demo Complete!")
        print("\n✓ All demos completed successfully!")
        print("✓ Framework is working as expected")
        print("\nKey Features Demonstrated:")
        print("  • Deterministic similarity scoring")
        print("  • Explainable results with breakdowns")
        print("  • Batch duplicate detection")
        print("  • No AI dependencies for core functionality")
        print("\nNext Steps:")
        print("  • Try examples/custom_vocabulary.py to add custom tags")
        print("  • Run tests with: python3 -m pytest tests/ (requires pytest)")
        print("  • Explore the vocabularies/ folder to customize behavior")
        print()
        
    except Exception as e:
        print(f"\n✗ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
