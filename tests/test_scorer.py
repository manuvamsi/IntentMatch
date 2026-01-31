"""
Test suite for the SimilarityScorer (Layer 4).
"""

import pytest
from iif import SimilarityScorer


class TestSimilarityScorer:
    
    def setup_method(self):
        """Set up test fixtures."""
        self.scorer = SimilarityScorer()
    
    def test_identical_prompts(self):
        """Test that identical prompts have high similarity."""
        prompt = "You are a helpful assistant."
        result = self.scorer.compare(prompt, prompt)
        
        assert result['similarity_score'] >= 0.9
        assert result['verdict'] == 'high_similarity'
    
    def test_similar_roleplay_prompts(self):
        """Test similar roleplay prompts."""
        prompt1 = "You are Sheldon Cooper. Always use Bazinga!"
        prompt2 = "Act as Sheldon Cooper. Use the catchphrase Bazinga!"
        
        result = self.scorer.compare(prompt1, prompt2)
        
        assert result['similarity_score'] >= 0.65
        assert 'roleplay' in result['explanation']['matched_tags']
    
    def test_different_prompts(self):
        """Test completely different prompts."""
        prompt1 = "Write a poem about nature."
        prompt2 = "Extract email addresses from text."
        
        result = self.scorer.compare(prompt1, prompt2)
        
        assert result['similarity_score'] < 0.5
        assert result['verdict'] in ['low_similarity', 'no_similarity']
    
    def test_explanation_structure(self):
        """Test that explanation has required fields."""
        prompt1 = "Test prompt 1"
        prompt2 = "Test prompt 2"
        
        result = self.scorer.compare(prompt1, prompt2)
        
        assert 'matched_tags' in result['explanation']
        assert 'matched_patterns' in result['explanation']
        assert 'structural_differences' in result['explanation']
        assert 'key_similarities' in result['explanation']
        assert 'key_differences' in result['explanation']
    
    def test_breakdown_components(self):
        """Test that breakdown has all components."""
        prompt1 = "Test prompt 1"
        prompt2 = "Test prompt 2"
        
        result = self.scorer.compare(prompt1, prompt2)
        
        assert 'structural' in result['breakdown']
        assert 'tag_overlap' in result['breakdown']
        assert 'pattern_match' in result['breakdown']
        assert all(0 <= v <= 1 for v in result['breakdown'].values())
    
    def test_verdict_categories(self):
        """Test that verdict is one of expected categories."""
        prompt1 = "Test prompt"
        prompt2 = "Another test"
        
        result = self.scorer.compare(prompt1, prompt2)
        
        valid_verdicts = ['high_similarity', 'moderate_similarity', 'low_similarity', 'no_similarity']
        assert result['verdict'] in valid_verdicts
    
    def test_same_goal_similarity(self):
        """Test that prompts with same goal have higher similarity."""
        prompt1 = "Write a story about dragons."
        prompt2 = "Create a tale about knights."
        
        result = self.scorer.compare(prompt1, prompt2)
        
        # Both are creative writing tasks
        assert result['similarity_score'] > 0.3
    
    def test_details_included(self):
        """Test that detailed analysis is included."""
        prompt1 = "Test prompt 1"
        prompt2 = "Test prompt 2"
        
        result = self.scorer.compare(prompt1, prompt2)
        
        assert 'details' in result
        assert 'canonical1' in result['details']
        assert 'canonical2' in result['details']
        assert 'fingerprint1' in result['details']
        assert 'fingerprint2' in result['details']
