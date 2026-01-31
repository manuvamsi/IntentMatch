"""
Test suite for the Canonicalizer (Layer 1).
"""

import pytest
from iif.canonicalizer import Canonicalizer


class TestCanonicalizer:
    
    def setup_method(self):
        """Set up test fixtures."""
        self.canonicalizer = Canonicalizer()
    
    def test_basic_roleplay_prompt(self):
        """Test canonicalization of a basic roleplay prompt."""
        text = "You are Sherlock Holmes. Always use deductive reasoning."
        result = self.canonicalizer.canonicalize(text)
        
        assert result['type'] == 'prompt'
        assert 'sherlock' in result['roles']
        assert len(result['constraints']) > 0
        assert result['goal'] == 'roleplay'
    
    def test_extract_roles(self):
        """Test role extraction."""
        text = "Act as a helpful assistant and pretend to be a teacher."
        result = self.canonicalizer.canonicalize(text)
        
        assert 'assistant' in result['roles'] or 'teacher' in result['roles']
        assert len(result['roles']) > 0
    
    def test_extract_constraints(self):
        """Test constraint extraction."""
        text = "You must always respond politely. Never use slang."
        result = self.canonicalizer.canonicalize(text)
        
        assert 'strict_behavior' in result['constraints'] or 'prohibition' in result['constraints']
    
    def test_catchphrase_detection(self):
        """Test catchphrase constraint detection."""
        text = "Use the catchphrase 'Bazinga!' when making jokes."
        result = self.canonicalizer.canonicalize(text)
        
        assert 'catchphrase_required' in result['constraints']
    
    def test_interaction_pattern_detection(self):
        """Test interaction pattern detection."""
        text = "User: Hello\nAssistant: Hi there!"
        result = self.canonicalizer.canonicalize(text)
        
        assert result['interaction_pattern'] == 'conversational'
    
    def test_length_categorization(self):
        """Test length categorization."""
        short_text = "Write a poem."
        long_text = " ".join(["This is a very long prompt."] * 50)
        
        short_result = self.canonicalizer.canonicalize(short_text)
        long_result = self.canonicalizer.canonicalize(long_text)
        
        assert short_result['metadata']['length'] == 'short'
        assert long_result['metadata']['length'] == 'long'
    
    def test_goal_inference(self):
        """Test goal inference from content."""
        creative_text = "Write a creative story about robots."
        qa_text = "Answer the following question: What is AI?"
        
        creative_result = self.canonicalizer.canonicalize(creative_text)
        qa_result = self.canonicalizer.canonicalize(qa_text)
        
        assert creative_result['goal'] == 'generation'
        assert qa_result['goal'] == 'question_answering'
    
    def test_empty_input(self):
        """Test handling of empty input."""
        result = self.canonicalizer.canonicalize("")
        
        assert result['type'] == 'prompt'
        assert result['roles'] == []
        assert result['goal'] == 'general'
    
    def test_metadata_preservation(self):
        """Test that provided metadata is preserved."""
        text = "Test prompt"
        metadata = {"source": "test", "author": "tester"}
        
        result = self.canonicalizer.canonicalize(text, metadata)
        
        assert result['metadata']['source'] == 'test'
        assert result['metadata']['author'] == 'tester'
