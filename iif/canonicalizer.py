"""
Layer 1: Canonicalization Engine

Converts prompts and datasets into normalized, structured representations.
"""

import re
from typing import Dict, List, Any, Optional
from .utils import normalize_text, extract_keywords, load_vocabulary


class Canonicalizer:
    """
    Canonicalizes prompts/datasets into structured intent representations.
    """
    
    def __init__(self):
        """Initialize the canonicalizer with vocabularies."""
        self.synonyms = load_vocabulary("synonyms")
        self.patterns = load_vocabulary("patterns")
    
    def canonicalize(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Convert a prompt/dataset into canonical form.
        
        Args:
            text: The prompt or dataset text
            metadata: Optional metadata about the input
            
        Returns:
            Canonical representation as a dictionary
        """
        normalized = normalize_text(text)
        
        return {
            "type": self._detect_type(text, metadata),
            "roles": self._extract_roles(normalized),
            "constraints": self._extract_constraints(normalized),
            "goal": self._extract_goal(normalized),
            "interaction_pattern": self._detect_interaction_pattern(text),
            "metadata": self._extract_metadata(text, metadata)
        }
    
    def _detect_type(self, text: str, metadata: Optional[Dict[str, Any]]) -> str:
        """Detect if input is a prompt, dataset, or other type."""
        if metadata and "type" in metadata:
            return metadata["type"]
        
        # Simple heuristic: if it contains multiple examples, it's likely a dataset
        if text.count("example:") > 2 or text.count("input:") > 2:
            return "dataset"
        
        return "prompt"
    
    def _extract_roles(self, text: str) -> List[str]:
        """Extract roles/personas from the text."""
        roles = []
        
        # Look for role indicators
        role_patterns = [
            r"act as (?:a |an )?(\w+)",
            r"you are (?:a |an )?(\w+)",
            r"pretend to be (?:a |an )?(\w+)",
            r"role(?:play)? (?:as )?(?:a |an )?(\w+)",
            r"persona:\s*(\w+)",
        ]
        
        for pattern in role_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            roles.extend(matches)
        
        # Deduplicate and normalize
        return list(set([r.lower() for r in roles]))
    
    def _extract_constraints(self, text: str) -> List[str]:
        """Extract constraints/rules from the text."""
        constraints = []
        
        # Look for constraint indicators
        constraint_keywords = [
            "always", "never", "must", "should", "cannot", "should not",
            "only", "strict", "required", "forbidden"
        ]
        
        # Find sentences containing constraint keywords
        sentences = re.split(r'[.!?]', text)
        for sentence in sentences:
            for keyword in constraint_keywords:
                if keyword in sentence.lower():
                    # Extract the constraint type
                    if "always" in sentence.lower():
                        constraints.append("strict_behavior")
                    elif "never" in sentence.lower() or "cannot" in sentence.lower():
                        constraints.append("prohibition")
                    elif "must" in sentence.lower() or "required" in sentence.lower():
                        constraints.append("requirement")
                    break
        
        # Look for specific patterns
        if re.search(r"catchphrase|signature phrase", text, re.IGNORECASE):
            constraints.append("catchphrase_required")
        
        return list(set(constraints))
    
    def _extract_goal(self, text: str) -> str:
        """Extract the primary goal/objective."""
        # Check for explicit goal statements
        goal_patterns = [
            r"goal:\s*(\w+)",
            r"objective:\s*(\w+)",
            r"purpose:\s*(\w+)",
        ]
        
        for pattern in goal_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).lower()
        
        # Infer goal from content
        if any(kw in text for kw in ["roleplay", "act as", "pretend"]):
            return "roleplay"
        elif any(kw in text for kw in ["write", "create", "generate"]):
            return "generation"
        elif any(kw in text for kw in ["answer", "respond", "explain"]):
            return "question_answering"
        elif any(kw in text for kw in ["extract", "parse", "identify"]):
            return "extraction"
        
        return "general"
    
    def _detect_interaction_pattern(self, text: str) -> str:
        """Detect the interaction pattern."""
        for pattern_name, pattern_data in self.patterns.items():
            indicators = pattern_data.get("indicators", [])
            if any(indicator in text.lower() for indicator in indicators):
                return pattern_name
        
        return "unstructured"
    
    def _extract_metadata(self, text: str, provided_metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract metadata about the prompt."""
        metadata = provided_metadata.copy() if provided_metadata else {}
        
        # Calculate length category
        word_count = len(text.split())
        if word_count < 50:
            metadata["length"] = "short"
        elif word_count < 200:
            metadata["length"] = "medium"
        else:
            metadata["length"] = "long"
        
        # Estimate complexity based on structure
        complexity_score = 0
        complexity_score += len(re.findall(r'[.!?]', text)) * 0.5  # Sentence count
        complexity_score += len(re.findall(r'\n', text)) * 0.3  # Line breaks
        complexity_score += len(re.findall(r'[:\-\*]', text)) * 0.2  # Structural markers
        
        if complexity_score < 5:
            metadata["complexity"] = "simple"
        elif complexity_score < 15:
            metadata["complexity"] = "moderate"
        else:
            metadata["complexity"] = "complex"
        
        return metadata
