"""
Layer 4: Similarity Scoring

Computes deterministic similarity scores with explanations.
"""

from typing import Dict, List, Any, Tuple
from .canonicalizer import Canonicalizer
from .fingerprinter import Fingerprinter
from .tagger import IntentTagger


class SimilarityScorer:
    """
    Computes similarity between prompts with detailed explanations.
    """
    
    def __init__(self):
        """Initialize the scorer with all required components."""
        self.canonicalizer = Canonicalizer()
        self.fingerprinter = Fingerprinter()
        self.tagger = IntentTagger()
    
    def compare(self, text1: str, text2: str, 
                metadata1: Dict[str, Any] = None,
                metadata2: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Compare two prompts and return detailed similarity analysis.
        
        Args:
            text1: First prompt text
            text2: Second prompt text
            metadata1: Optional metadata for first prompt
            metadata2: Optional metadata for second prompt
            
        Returns:
            Detailed similarity report
        """
        # Canonicalize both inputs
        canonical1 = self.canonicalizer.canonicalize(text1, metadata1)
        canonical2 = self.canonicalizer.canonicalize(text2, metadata2)
        
        # Generate fingerprints
        fingerprint1 = self.fingerprinter.fingerprint(canonical1)
        fingerprint2 = self.fingerprinter.fingerprint(canonical2)
        
        # Generate tags
        tags1 = self.tagger.tag(canonical1, text1)
        tags2 = self.tagger.tag(canonical2, text2)
        
        # Calculate component similarities
        structural_sim = self.fingerprinter.compare_fingerprints(fingerprint1, fingerprint2)
        tag_sim, matched_tags = self.tagger.compare_tags(tags1, tags2)
        pattern_sim = self._compare_patterns(canonical1, canonical2)
        
        # Calculate overall similarity (weighted combination)
        overall_similarity = (
            structural_sim * 0.3 +
            tag_sim * 0.5 +
            pattern_sim * 0.2
        )
        
        # Generate explanation
        explanation = self._generate_explanation(
            canonical1, canonical2,
            fingerprint1, fingerprint2,
            tags1, tags2,
            matched_tags
        )
        
        # Determine verdict
        verdict = self._determine_verdict(overall_similarity)
        
        return {
            "similarity_score": round(overall_similarity, 3),
            "breakdown": {
                "structural": round(structural_sim, 3),
                "tag_overlap": round(tag_sim, 3),
                "pattern_match": round(pattern_sim, 3)
            },
            "explanation": explanation,
            "verdict": verdict,
            "details": {
                "canonical1": canonical1,
                "canonical2": canonical2,
                "fingerprint1": fingerprint1,
                "fingerprint2": fingerprint2,
                "tags1": tags1,
                "tags2": tags2
            }
        }
    
    def _compare_patterns(self, canonical1: Dict[str, Any], canonical2: Dict[str, Any]) -> float:
        """Compare interaction patterns between two canonicals."""
        pattern1 = canonical1.get("interaction_pattern", "unstructured")
        pattern2 = canonical2.get("interaction_pattern", "unstructured")
        
        if pattern1 == pattern2:
            return 1.0
        
        # Some patterns are similar
        similar_patterns = {
            "conversational": ["instructional"],
            "instructional": ["conversational", "example_based"],
            "template": ["list"],
            "list": ["template"]
        }
        
        if pattern2 in similar_patterns.get(pattern1, []):
            return 0.6
        
        return 0.0
    
    def _generate_explanation(self, canonical1: Dict[str, Any], canonical2: Dict[str, Any],
                            fingerprint1: Dict[str, Any], fingerprint2: Dict[str, Any],
                            tags1: Dict[str, Any], tags2: Dict[str, Any],
                            matched_tags: List[str]) -> Dict[str, Any]:
        """Generate human-readable explanation of similarity."""
        explanation = {
            "matched_tags": matched_tags,
            "matched_patterns": [],
            "structural_differences": [],
            "key_similarities": [],
            "key_differences": []
        }
        
        # Pattern matching
        if canonical1.get("interaction_pattern") == canonical2.get("interaction_pattern"):
            explanation["matched_patterns"].append(canonical1.get("interaction_pattern"))
        
        # Structural differences
        role_diff = abs(fingerprint1.get("role_count", 0) - fingerprint2.get("role_count", 0))
        if role_diff > 0:
            explanation["structural_differences"].append(
                f"role_count: {fingerprint1.get('role_count')} vs {fingerprint2.get('role_count')}"
            )
        
        constraint_diff = abs(fingerprint1.get("constraint_count", 0) - fingerprint2.get("constraint_count", 0))
        if constraint_diff > 0:
            explanation["structural_differences"].append(
                f"constraint_count: {fingerprint1.get('constraint_count')} vs {fingerprint2.get('constraint_count')}"
            )
        
        # Key similarities
        if canonical1.get("goal") == canonical2.get("goal"):
            explanation["key_similarities"].append(f"Same goal: {canonical1.get('goal')}")
        
        if fingerprint1.get("has_roles") and fingerprint2.get("has_roles"):
            explanation["key_similarities"].append("Both define roles/personas")
        
        if fingerprint1.get("has_constraints") and fingerprint2.get("has_constraints"):
            explanation["key_similarities"].append("Both have constraints")
        
        # Key differences
        if canonical1.get("goal") != canonical2.get("goal"):
            explanation["key_differences"].append(
                f"Different goals: {canonical1.get('goal')} vs {canonical2.get('goal')}"
            )
        
        if fingerprint1.get("complexity_score", 0) - fingerprint2.get("complexity_score", 0) > 3:
            explanation["key_differences"].append("Significantly different complexity levels")
        
        return explanation
    
    def _determine_verdict(self, similarity: float) -> str:
        """Determine verdict based on similarity score."""
        if similarity >= 0.85:
            return "high_similarity"
        elif similarity >= 0.65:
            return "moderate_similarity"
        elif similarity >= 0.40:
            return "low_similarity"
        else:
            return "no_similarity"
    
    def batch_compare(self, prompts: List[Tuple[str, str]], 
                     threshold: float = 0.65) -> List[Dict[str, Any]]:
        """
        Compare multiple prompt pairs in batch.
        
        Args:
            prompts: List of (text1, text2) tuples
            threshold: Minimum similarity to report
            
        Returns:
            List of similarity reports for pairs above threshold
        """
        results = []
        
        for i, (text1, text2) in enumerate(prompts):
            result = self.compare(text1, text2)
            if result["similarity_score"] >= threshold:
                result["pair_index"] = i
                results.append(result)
        
        return results
