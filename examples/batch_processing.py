"""
Batch processing example for the Intent Identity Framework.

This example shows how to find duplicates in a dataset of prompts.
"""

from iif import SimilarityScorer
import json


def main():
    # Initialize the scorer
    scorer = SimilarityScorer()
    
    # Sample dataset of prompts
    prompts = [
        "You are a helpful AI assistant. Answer questions clearly and concisely.",
        "Act as a helpful assistant. Provide clear and concise answers to user questions.",
        "Write a poem about nature in the style of Robert Frost.",
        "Generate a nature poem inspired by Robert Frost's writing style.",
        "Extract all dates from the text and format them as YYYY-MM-DD.",
        "You are Sherlock Holmes. Use deductive reasoning and stay in character.",
        "Parse the text and identify all date mentions, converting to YYYY-MM-DD format.",
        "Roleplay as Sherlock Holmes. Always use logical deduction and maintain character.",
    ]
    
    print("Finding duplicates in dataset...")
    print(f"Total prompts: {len(prompts)}\n")
    
    # Find all pairs with similarity > 0.65
    duplicates = []
    
    for i in range(len(prompts)):
        for j in range(i + 1, len(prompts)):
            result = scorer.compare(prompts[i], prompts[j])
            
            if result['similarity_score'] >= 0.65:
                duplicates.append({
                    'index1': i,
                    'index2': j,
                    'prompt1': prompts[i][:50] + "...",
                    'prompt2': prompts[j][:50] + "...",
                    'similarity': result['similarity_score'],
                    'verdict': result['verdict'],
                    'matched_tags': result['explanation']['matched_tags']
                })
    
    # Display results
    print(f"Found {len(duplicates)} potential duplicates:\n")
    
    for dup in duplicates:
        print(f"Pair ({dup['index1']}, {dup['index2']}): {dup['similarity']:.3f} - {dup['verdict']}")
        print(f"  Prompt 1: {dup['prompt1']}")
        print(f"  Prompt 2: {dup['prompt2']}")
        print(f"  Matched Tags: {dup['matched_tags']}")
        print()
    
    # Save results
    with open("duplicates_report.json", "w") as f:
        json.dump(duplicates, f, indent=2)
    
    print(f"Full report saved to duplicates_report.json")
    
    # Statistics
    print("\nStatistics:")
    print(f"  Total comparisons: {len(prompts) * (len(prompts) - 1) // 2}")
    print(f"  Duplicates found: {len(duplicates)}")
    print(f"  Duplication rate: {len(duplicates) / (len(prompts) * (len(prompts) - 1) // 2) * 100:.1f}%")


if __name__ == "__main__":
    main()
