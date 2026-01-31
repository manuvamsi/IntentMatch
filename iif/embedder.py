"""
Layer 5: Optional Embedding Filter

Lightweight semantic filter for edge cases (optional dependency).
"""

from typing import List, Optional
import warnings


class Embedder:
    """
    Optional semantic similarity using lightweight embeddings.
    Only used when rule-based methods are inconclusive.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedder with a lightweight model.
        
        Args:
            model_name: Name of the sentence-transformers model
        """
        self.model = None
        self.model_name = model_name
        self._initialize_model()
    
    def _initialize_model(self):
        """Lazy initialization of the embedding model."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
        except ImportError:
            warnings.warn(
                "sentence-transformers not installed. "
                "Embedding filter will not be available. "
                "Install with: pip install sentence-transformers"
            )
            self.model = None
    
    def is_available(self) -> bool:
        """Check if embedding functionality is available."""
        return self.model is not None
    
    def embed(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector or None if unavailable
        """
        if not self.is_available():
            return None
        
        return self.model.encode(text).tolist()
    
    def similarity(self, text1: str, text2: str) -> Optional[float]:
        """
        Calculate semantic similarity between two texts.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0.0 to 1.0) or None if unavailable
        """
        if not self.is_available():
            return None
        
        from sentence_transformers import util
        
        emb1 = self.model.encode(text1)
        emb2 = self.model.encode(text2)
        
        similarity = util.cos_sim(emb1, emb2).item()
        
        # Normalize to 0-1 range (cosine similarity is -1 to 1)
        return (similarity + 1) / 2
    
    def should_use_embedding(self, rule_based_score: float, 
                            confidence: float = 0.8) -> bool:
        """
        Determine if embedding filter should be used.
        
        Args:
            rule_based_score: Score from rule-based methods
            confidence: Confidence threshold
            
        Returns:
            True if embedding should be used as tiebreaker
        """
        # Use embeddings only in inconclusive cases
        # (scores near decision boundaries)
        if 0.35 <= rule_based_score <= 0.45:
            return True
        if 0.60 <= rule_based_score <= 0.70:
            return True
        if 0.80 <= rule_based_score <= 0.90:
            return True
        
        return False
