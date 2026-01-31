# Contributing to Intent Identity Framework

Thank you for your interest in contributing! This project is designed to be **community-driven**, and we welcome contributions of all kinds.

## How to Contribute

### 1. Extending Vocabularies (Easiest)

The most accessible way to contribute is by extending our vocabularies:

#### Adding Intent Tags

Edit `vocabularies/intent_tags.json`:

```json
{
  "your_tag_name": {
    "description": "Clear description of what this tag represents",
    "rules": {
      "required": ["field_name"],  // Required canonical fields
      "keywords": ["keyword1", "keyword2"]  // Keywords to match
    },
    "parent": null  // Optional parent tag for hierarchy
  }
}
```

**Example:**
```json
{
  "sentiment_analysis": {
    "description": "Analyzes emotional tone or sentiment",
    "rules": {
      "required": ["goal"],
      "keywords": ["sentiment", "emotion", "tone", "feeling", "mood"]
    },
    "parent": "data_extraction"
  }
}
```

#### Adding Structural Patterns

Edit `vocabularies/patterns.json`:

```json
{
  "your_pattern": {
    "description": "Pattern description",
    "indicators": ["indicator1", "indicator2"]
  }
}
```

#### Adding Synonyms

Edit `vocabularies/synonyms.json`:

```json
{
  "concept": ["synonym1", "synonym2", "synonym3"]
}
```

### 2. Improving Core Layers

#### Layer 1: Canonicalization
- Improve role extraction patterns
- Add new constraint detection rules
- Enhance goal inference logic

File: `iif/canonicalizer.py`

#### Layer 2: Fingerprinting
- Add new structural features
- Improve complexity scoring
- Enhance fingerprint comparison

File: `iif/fingerprinter.py`

#### Layer 3: Intent Tagging
- Improve tag evaluation logic
- Add tag hierarchy support
- Enhance confidence scoring

File: `iif/tagger.py`

#### Layer 4: Similarity Scoring
- Adjust similarity weights
- Improve explanation generation
- Add new comparison metrics

File: `iif/scorer.py`

### 3. Adding Tests

We use pytest for testing. Add tests in `tests/`:

```python
def test_your_feature():
    """Test description."""
    # Your test code
    assert expected == actual
```

Run tests:
```bash
python3 -m pytest tests/ -v
```

### 4. Adding Examples

Create new examples in `examples/`:

```python
"""
Description of what this example demonstrates.
"""

from iif import SimilarityScorer

def main():
    # Your example code
    pass

if __name__ == "__main__":
    main()
```

## Development Setup

### Option 1: Direct Development
```bash
cd DuplicateDetector
python3 demo.py  # Test your changes
```

### Option 2: Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
python3 -m pytest tests/
```

## Code Style

- Follow PEP 8 guidelines
- Use descriptive variable names
- Add docstrings to all functions
- Keep functions focused and small

## Commit Messages

Use clear, descriptive commit messages:

```
Add sentiment analysis intent tag

- Added new tag to vocabularies/intent_tags.json
- Updated tests to cover sentiment analysis
- Added example in examples/sentiment_demo.py
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Test your changes (`python3 demo.py`)
5. Commit your changes
6. Push to your fork
7. Create a Pull Request

## Areas Needing Help

### High Priority
- [ ] More intent tags for common use cases
- [ ] Additional test cases
- [ ] Performance benchmarking
- [ ] Documentation improvements

### Medium Priority
- [ ] Web API wrapper
- [ ] CLI tool
- [ ] Visualization tools
- [ ] Integration examples

### Future Enhancements
- [ ] Version lineage tracking
- [ ] Bias detection
- [ ] Prompt evolution graphs
- [ ] IDE plugins

## Questions?

Open an issue on GitHub or start a discussion!

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).
