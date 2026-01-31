"""
Shared utility functions for the IIF framework.
"""

import re
import json
from typing import Any, Dict, List
from pathlib import Path


def load_vocabulary(vocab_name: str) -> Dict[str, Any]:
    """
    Load a vocabulary file from the vocabularies directory.
    
    Args:
        vocab_name: Name of the vocabulary file (without .json extension)
        
    Returns:
        Dictionary containing the vocabulary data
    """
    vocab_path = Path(__file__).parent.parent / "vocabularies" / f"{vocab_name}.json"
    
    if not vocab_path.exists():
        raise FileNotFoundError(f"Vocabulary file not found: {vocab_path}")
    
    with open(vocab_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def normalize_text(text: str) -> str:
    """
    Normalize text by removing extra whitespace and converting to lowercase.
    
    Args:
        text: Input text to normalize
        
    Returns:
        Normalized text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    # Convert to lowercase
    text = text.lower()
    return text


def extract_keywords(text: str, keywords: List[str]) -> List[str]:
    """
    Extract matching keywords from text.
    
    Args:
        text: Text to search in
        keywords: List of keywords to search for
        
    Returns:
        List of found keywords
    """
    normalized = normalize_text(text)
    found = []
    
    for keyword in keywords:
        if normalize_text(keyword) in normalized:
            found.append(keyword)
    
    return found


def jaccard_similarity(set1: set, set2: set) -> float:
    """
    Calculate Jaccard similarity between two sets.
    
    Args:
        set1: First set
        set2: Second set
        
    Returns:
        Jaccard similarity score (0.0 to 1.0)
    """
    if not set1 and not set2:
        return 1.0
    
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Cosine similarity score (-1.0 to 1.0)
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same length")
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)
