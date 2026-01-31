"""
Layer 3: Intent Tagging System

Maps canonical representations to controlled intent tags.
"""

from typing import Dict, List, Any, Tuple
from .utils import load_vocabulary, extract_keywords


class IntentTagger:
    """
    Tags canonical representations with intent labels.
    """
    
    def __init__(self):
        """Initialize the tagger with intent vocabulary."""
        self.intent_tags = load_vocabulary("intent_tags")
    
    def tag(self, canonical: Dict[str, Any], text: str = "") -> Dict[str, Any]:
        """
        Assign intent tags to a canonical representation.
        
        Args:
            canonical: Canonical representation from Canonicalizer
            text: Original text (optional, for keyword matching)
            
        Returns:
            Dictionary with primary tags, secondary tags, and confidence scores
        """
        tag_scores = {}
        
        # Evaluate each tag
        for tag_name, tag_data in self.intent_tags.items():
            score = self._evaluate_tag(tag_name, tag_data, canonical, text)
            if score > 0:
                tag_scores[tag_name] = score
        
        # Sort by score
        sorted_tags = sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Separate primary and secondary tags
        primary_tags = [tag for tag, score in sorted_tags if score >= 0.7]
        secondary_tags = [tag for tag, score in sorted_tags if 0.3 <= score < 0.7]
        
        return {
            "primary_tags": primary_tags,
            "secondary_tags": secondary_tags,
            "confidence": dict(sorted_tags)
        }
    
    def _evaluate_tag(self, tag_name: str, tag_data: Dict[str, Any], 
                     canonical: Dict[str, Any], text: str) -> float:
        """
        Evaluate how well a tag matches the canonical representation.
        
        Returns:
            Confidence score (0.0 to 1.0)
        """
        score = 0.0
        rules = tag_data.get("rules", {})
        
        # Check required fields
        required = rules.get("required", [])
        required_met = 0
        for field in required:
            if field in canonical and canonical[field]:
                required_met += 1
        
        if required:
            required_score = required_met / len(required)
            if required_score == 0:
                return 0.0  # If required fields not met, tag doesn't apply
            score += required_score * 0.6
        else:
            score += 0.3  # Base score if no requirements
        
        # Check keywords
        keywords = rules.get("keywords", [])
        if keywords and text:
            found_keywords = extract_keywords(text, keywords)
            if found_keywords:
                keyword_score = len(found_keywords) / len(keywords)
                score += keyword_score * 0.4
        
        return min(score, 1.0)
    
    def compare_tags(self, tags1: Dict[str, Any], tags2: Dict[str, Any]) -> Tuple[float, List[str]]:
        """
        Compare two tag sets and return similarity.
        
        Args:
            tags1: First tag set
            tags2: Second tag set
            
        Returns:
            Tuple of (similarity_score, matched_tags)
        """
        primary1 = set(tags1.get("primary_tags", []))
        primary2 = set(tags2.get("primary_tags", []))
        
        secondary1 = set(tags1.get("secondary_tags", []))
        secondary2 = set(tags2.get("secondary_tags", []))
        
        # Calculate Jaccard similarity for primary tags (weighted more)
        primary_intersection = primary1.intersection(primary2)
        primary_union = primary1.union(primary2)
        
        if primary_union:
            primary_similarity = len(primary_intersection) / len(primary_union)
        else:
            primary_similarity = 0.0
        
        # Calculate Jaccard similarity for secondary tags
        secondary_intersection = secondary1.intersection(secondary2)
        secondary_union = secondary1.union(secondary2)
        
        if secondary_union:
            secondary_similarity = len(secondary_intersection) / len(secondary_union)
        else:
            secondary_similarity = 0.0
        
        # Weighted combination (primary tags matter more)
        overall_similarity = (primary_similarity * 0.7) + (secondary_similarity * 0.3)
        
        # Get matched tags
        matched_tags = list(primary_intersection.union(secondary_intersection))
        
        return overall_similarity, matched_tags
