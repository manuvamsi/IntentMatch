"""
Dataset Duplicate Checker

This script analyzes JSON datasets to find duplicate conversations
based on intent-level similarity.

Usage:
    python3 check_sheldon_duplicates.py [dataset.json]
    
    If no file is specified, defaults to 'sheldon.json'
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from iif import SimilarityScorer
from collections import defaultdict


def load_sheldon_dataset(filepath):
    """Load the Sheldon dataset from JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_conversations(dataset):
    """Extract user-assistant conversation pairs."""
    conversations = []
    
    for idx, item in enumerate(dataset):
        messages = item.get('messages', [])
        
        # Extract user and assistant messages
        user_msgs = []
        assistant_msgs = []
        
        for msg in messages:
            role = msg.get('role', '')
            content = msg.get('content', '')
            
            if role == 'user':
                user_msgs.append(content)
            elif role == 'assistant':
                assistant_msgs.append(content)
        
        # Combine into conversation text
        conversation = {
            'index': idx,
            'user': ' '.join(user_msgs),
            'assistant': ' '.join(assistant_msgs),
            'full': ' '.join(user_msgs) + ' ' + ' '.join(assistant_msgs)
        }
        
        conversations.append(conversation)
    
    return conversations


def find_duplicates(conversations, threshold=0.75, sample_size=None):
    """
    Find duplicate conversations based on similarity.
    
    Args:
        conversations: List of conversation dictionaries
        threshold: Similarity threshold (0.0 to 1.0)
        sample_size: If set, only check first N conversations (for testing)
    """
    scorer = SimilarityScorer()
    
    # Limit sample size if specified
    if sample_size:
        conversations = conversations[:sample_size]
        print(f"📊 Analyzing first {sample_size} conversations (sample mode)")
    else:
        print(f"📊 Analyzing all {len(conversations)} conversations")
    
    print(f"🎯 Similarity threshold: {threshold * 100}%\n")
    
    duplicates = []
    total_comparisons = len(conversations) * (len(conversations) - 1) // 2
    
    print(f"⏳ Total comparisons to make: {total_comparisons:,}")
    print("🔍 Checking for duplicates...\n")
    
    # Progress tracking
    checked = 0
    
    for i in range(len(conversations)):
        for j in range(i + 1, len(conversations)):
            # Compare full conversation text
            result = scorer.compare(
                conversations[i]['full'],
                conversations[j]['full']
            )
            
            checked += 1
            
            # Progress indicator every 100 comparisons
            if checked % 100 == 0:
                print(f"  Checked {checked:,}/{total_comparisons:,} pairs...", end='\r')
            
            if result['similarity_score'] >= threshold:
                duplicates.append({
                    'index1': conversations[i]['index'],
                    'index2': conversations[j]['index'],
                    'similarity': result['similarity_score'],
                    'verdict': result['verdict'],
                    'user1': conversations[i]['user'][:100],
                    'user2': conversations[j]['user'][:100],
                    'assistant1': conversations[i]['assistant'][:100],
                    'assistant2': conversations[j]['assistant'][:100],
                    'matched_tags': result['explanation']['matched_tags']
                })
    
    print(f"  Checked {checked:,}/{total_comparisons:,} pairs... Done!     \n")
    
    return duplicates


def print_results(duplicates, total_conversations):
    """Print duplicate detection results."""
    print("\n" + "=" * 70)
    print("  DUPLICATE DETECTION RESULTS")
    print("=" * 70)
    
    if not duplicates:
        print("\n✅ No duplicates found! Dataset is clean.\n")
        return
    
    print(f"\n⚠️  Found {len(duplicates)} potential duplicate pairs:\n")
    
    # Group by similarity level
    high_sim = [d for d in duplicates if d['similarity'] >= 0.85]
    moderate_sim = [d for d in duplicates if 0.75 <= d['similarity'] < 0.85]
    
    if high_sim:
        print(f"🔴 High Similarity (≥85%): {len(high_sim)} pairs")
    if moderate_sim:
        print(f"🟡 Moderate Similarity (75-85%): {len(moderate_sim)} pairs")
    
    print("\n" + "-" * 70)
    print("Top 10 Duplicates:")
    print("-" * 70)
    
    # Show top 10
    for idx, dup in enumerate(sorted(duplicates, key=lambda x: x['similarity'], reverse=True)[:10], 1):
        print(f"\n{idx}. Pair ({dup['index1']}, {dup['index2']}): {dup['similarity']:.3f} ({dup['verdict'].replace('_', ' ').title()})")
        print(f"   User 1: {dup['user1']}...")
        print(f"   User 2: {dup['user2']}...")
        print(f"   Tags: {', '.join(dup['matched_tags'][:5])}")
    
    # Statistics
    print("\n" + "=" * 70)
    print("  STATISTICS")
    print("=" * 70)
    print(f"  Total conversations: {total_conversations}")
    print(f"  Duplicate pairs found: {len(duplicates)}")
    print(f"  Duplication rate: {len(duplicates) / (total_conversations * (total_conversations - 1) // 2) * 100:.2f}%")
    print(f"  Average similarity: {sum(d['similarity'] for d in duplicates) / len(duplicates):.3f}")
    print()


def save_report(duplicates, output_file='sheldon_duplicates_report.json'):
    """Save detailed report to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(duplicates, f, indent=2)
    print(f"📄 Detailed report saved to: {output_file}\n")


def remove_duplicates(dataset, duplicates):
    """
    Remove duplicate entries from dataset.
    Keeps the first occurrence, removes subsequent duplicates.
    
    Args:
        dataset: Original dataset
        duplicates: List of duplicate pairs
        
    Returns:
        Cleaned dataset and list of removed indices
    """
    # Collect all indices to remove (keep lower index, remove higher)
    indices_to_remove = set()
    
    for dup in duplicates:
        # Always remove the higher index to preserve order
        indices_to_remove.add(max(dup['index1'], dup['index2']))
    
    # Create cleaned dataset
    cleaned_dataset = [
        item for idx, item in enumerate(dataset)
        if idx not in indices_to_remove
    ]
    
    return cleaned_dataset, sorted(indices_to_remove)


def save_cleaned_dataset(cleaned_dataset, output_file='sheldon_cleaned.json'):
    """Save cleaned dataset to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_dataset, f, indent=2, ensure_ascii=False)
    print(f"✅ Cleaned dataset saved to: {output_file}")
    print(f"   Original entries: {len(cleaned_dataset) + len([])}")
    print(f"   Cleaned entries: {len(cleaned_dataset)}\n")


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("  DATASET DUPLICATE CHECKER")
    print("  Using Intent Identity Framework (IIF)")
    print("=" * 70 + "\n")
    
    # Get dataset filename from command line or use default
    if len(sys.argv) > 1:
        dataset_file = sys.argv[1]
    else:
        dataset_file = 'sheldon.json'
    
    # Check if file exists
    if not os.path.exists(dataset_file):
        print(f"❌ Error: File '{dataset_file}' not found!")
        print(f"\nUsage: python3 {sys.argv[0]} [dataset.json]")
        print(f"Example: python3 {sys.argv[0]} mydata.json")
        print(f"\nIf no file is specified, defaults to 'sheldon.json'\n")
        return
    
    # Load dataset
    print(f"📂 Loading {dataset_file}...")
    dataset = load_sheldon_dataset(dataset_file)
    print(f"✅ Loaded {len(dataset)} conversation entries\n")
    
    # Extract conversations
    print("🔄 Extracting conversations...")
    conversations = extract_conversations(dataset)
    print(f"✅ Extracted {len(conversations)} conversations\n")
    
    # Ask user for sample size
    print("Options:")
    print("  1. Quick test (first 50 conversations)")
    print("  2. Medium test (first 200 conversations)")
    print("  3. Full analysis (all conversations) - This will take time!")
    
    choice = input("\nEnter choice (1/2/3) [default: 1]: ").strip() or "1"
    
    sample_sizes = {"1": 50, "2": 200, "3": None}
    sample_size = sample_sizes.get(choice, 50)
    
    print()
    
    # Find duplicates
    duplicates = find_duplicates(conversations, threshold=0.75, sample_size=sample_size)
    
    # Print results
    print_results(duplicates, len(conversations) if not sample_size else sample_size)
    
    # Save report if duplicates found
    if duplicates:
        # Generate output filename based on input
        base_name = os.path.splitext(dataset_file)[0]
        report_file = f"{base_name}_duplicates_report.json"
        save_report(duplicates, report_file)
        
        # Ask if user wants to remove duplicates
        print("=" * 70)
        print("  DUPLICATE REMOVAL OPTIONS")
        print("=" * 70 + "\n")
        
        print("What would you like to do?")
        print("  1. Just show duplicates (already done)")
        print("  2. Remove duplicates and create cleaned dataset")
        print("  3. Exit without removing")
        
        action = input("\nEnter choice (1/2/3) [default: 1]: ").strip() or "1"
        
        if action == "2":
            print("\n🗑️  Removing duplicates...\n")
            
            # Remove duplicates
            cleaned_dataset, removed_indices = remove_duplicates(dataset, duplicates)
            
            print(f"✅ Removed {len(removed_indices)} duplicate entries")
            print(f"   Removed indices: {removed_indices[:10]}{'...' if len(removed_indices) > 10 else ''}\n")
            
            # Save cleaned dataset
            output_file = f"{base_name}_cleaned.json"
            save_cleaned_dataset(cleaned_dataset, output_file)
            
            print("=" * 70)
            print("✅ Duplicate removal complete!")
            print("=" * 70)
            print(f"\n📁 Files created:")
            print(f"   • {report_file} (duplicate analysis)")
            print(f"   • {output_file} (cleaned dataset)")
            print(f"\n💡 Original file '{dataset_file}' is unchanged.\n")
        else:
            print("\n✅ No changes made to dataset.\n")
    
    print("=" * 70)
    print("✅ Analysis complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

