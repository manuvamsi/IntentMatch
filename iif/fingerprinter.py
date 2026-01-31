"""
Layer 2: Structural Fingerprinting

Extracts shape-based features independent of content.
"""

from typing import Dict, List, Any
import math


class Fingerprinter:
    """
    Generates structural fingerprints for canonical representations.
    """
    
    def fingerprint(self, canonical: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a structural fingerprint from canonical representation.
        
        Args:
            canonical: Canonical representation from Canonicalizer
            
        Returns:
            Structural fingerprint dictionary
        """
        return {
            "role_count": len(canonical.get("roles", [])),
            "constraint_count": len(canonical.get("constraints", [])),
            "constraint_density": self._calculate_constraint_density(canonical),
            "interaction_pattern": canonical.get("interaction_pattern", "unstructured"),
            "complexity_score": self._calculate_complexity_score(canonical),
            "length_category": canonical.get("metadata", {}).get("length", "unknown"),
            "has_roles": len(canonical.get("roles", [])) > 0,
            "has_constraints": len(canonical.get("constraints", [])) > 0,
            "goal_type": canonical.get("goal", "general")
        }
    
    def _calculate_constraint_density(self, canonical: Dict[str, Any]) -> float:
        """
        Calculate the density of constraints relative to content.
        
        Higher density means more restrictive/specific prompts.
        """
        constraint_count = len(canonical.get("constraints", []))
        
        # Normalize by length category
        length = canonical.get("metadata", {}).get("length", "medium")
        length_weights = {
            "short": 1.0,
            "medium": 0.7,
            "long": 0.5
        }
        
        weight = length_weights.get(length, 0.7)
        return min(constraint_count * weight, 1.0)
    
    def _calculate_complexity_score(self, canonical: Dict[str, Any]) -> float:
        """
        Calculate overall complexity score (0-10 scale).
        """
        score = 0.0
        
        # Role complexity
        score += len(canonical.get("roles", [])) * 1.5
        
        # Constraint complexity
        score += len(canonical.get("constraints", [])) * 1.0
        
        # Interaction pattern complexity
        pattern = canonical.get("interaction_pattern", "unstructured")
        pattern_weights = {
            "unstructured": 0,
            "conversational": 2,
            "instructional": 3,
            "template": 2.5,
            "conditional": 4,
            "example_based": 3.5
        }
        score += pattern_weights.get(pattern, 1)
        
        # Metadata complexity
        metadata_complexity = canonical.get("metadata", {}).get("complexity", "simple")
        complexity_weights = {
            "simple": 0,
            "moderate": 2,
            "complex": 4
        }
        score += complexity_weights.get(metadata_complexity, 1)
        
        # Normalize to 0-10 scale
        return min(score, 10.0)
    
    def compare_fingerprints(self, fp1: Dict[str, Any], fp2: Dict[str, Any]) -> float:
        """
        Compare two fingerprints and return similarity score.
        
        Args:
            fp1: First fingerprint
            fp2: Second fingerprint
            
        Returns:
            Similarity score (0.0 to 1.0)
        """
        similarities = []
        
        # Exact matches
        if fp1.get("interaction_pattern") == fp2.get("interaction_pattern"):
            similarities.append(1.0)
        else:
            similarities.append(0.0)
        
        if fp1.get("goal_type") == fp2.get("goal_type"):
            similarities.append(1.0)
        else:
            similarities.append(0.5)  # Partial credit for different goals
        
        if fp1.get("length_category") == fp2.get("length_category"):
            similarities.append(1.0)
        else:
            similarities.append(0.7)  # Partial credit for different lengths
        
        # Numeric similarities
        role1 = fp1.get("role_count", 0)
        role2 = fp2.get("role_count", 0)
        if role1 == 0 and role2 == 0:
            role_sim = 1.0  # Both have no roles, perfect match
        elif role1 == 0 or role2 == 0:
            role_sim = 0.0  # One has roles, one doesn't
        else:
            role_sim = 1.0 - abs(role1 - role2) / max(role1, role2)
        similarities.append(role_sim)
        
        constraint1 = fp1.get("constraint_count", 0)
        constraint2 = fp2.get("constraint_count", 0)
        if constraint1 == 0 and constraint2 == 0:
            constraint_sim = 1.0  # Both have no constraints, perfect match
        elif constraint1 == 0 or constraint2 == 0:
            constraint_sim = 0.0  # One has constraints, one doesn't
        else:
            constraint_sim = 1.0 - abs(constraint1 - constraint2) / max(constraint1, constraint2)
        similarities.append(constraint_sim)
        
        density_sim = 1.0 - abs(fp1.get("constraint_density", 0) - fp2.get("constraint_density", 0))
        similarities.append(density_sim)
        
        complexity_sim = 1.0 - abs(fp1.get("complexity_score", 0) - fp2.get("complexity_score", 0)) / 10.0
        similarities.append(complexity_sim)
        
        # Boolean similarities
        if fp1.get("has_roles") == fp2.get("has_roles"):
            similarities.append(1.0)
        else:
            similarities.append(0.0)
        
        if fp1.get("has_constraints") == fp2.get("has_constraints"):
            similarities.append(1.0)
        else:
            similarities.append(0.0)
        
        # Return weighted average
        return sum(similarities) / len(similarities)
