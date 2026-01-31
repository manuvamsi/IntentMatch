"""
Intent Identity Framework (IIF)

An open-source framework to identify, deduplicate, and track 
intent-level similarity in AI prompts and datasets.
"""

__version__ = "0.1.0"
__author__ = "DuplicateDetector Contributors"

from .canonicalizer import Canonicalizer
from .fingerprinter import Fingerprinter
from .tagger import IntentTagger
from .scorer import SimilarityScorer

__all__ = [
    "Canonicalizer",
    "Fingerprinter", 
    "IntentTagger",
    "SimilarityScorer",
]
