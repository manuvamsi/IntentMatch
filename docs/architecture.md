# System Architecture

## Overview

The Intent Identity Framework (IIF) is a **5-layer architecture** designed to identify intent-level similarity in AI prompts and datasets without relying on large AI models.

## Layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Input (Text)                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Canonicalization Engine                       │
│  • Normalize text                                        │
│  • Extract roles, constraints, goals                     │
│  • Convert to structured JSON                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Structural Fingerprinting                      │
│  • Count structural elements                             │
│  • Calculate complexity scores                           │
│  • Generate shape-based features                         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Intent Tagging System                          │
│  • Apply rule-based tag matching                         │
│  • Use community-editable vocabularies                   │
│  • Generate confidence scores                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 4: Similarity Scoring                             │
│  • Combine structural, tag, and pattern similarity       │
│  • Generate explainable scores                           │
│  • Provide detailed breakdowns                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Layer 5: Optional Embedding Filter (Optional)           │
│  • Used only for edge cases                              │
│  • Lightweight semantic similarity                       │
│  • Requires sentence-transformers                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Similarity Report (JSON)                    │
│  • Overall score                                         │
│  • Component breakdown                                   │
│  • Explanation                                           │
└─────────────────────────────────────────────────────────┘
```

## Key Design Principles

### 1. Deterministic First
- Core functionality uses **no AI/ML models**
- Same input always produces same output
- Fully reproducible results

### 2. Explainable by Default
- Every similarity score includes:
  - Component breakdown (structural, tags, patterns)
  - Matched tags and patterns
  - Key similarities and differences
- No black-box decisions

### 3. Community-Driven Intelligence
- Intent tags defined in JSON files
- Anyone can extend vocabularies
- No code changes needed to add new concepts

### 4. Modular Architecture
- Each layer is independent
- Easy to swap or extend components
- Clear separation of concerns

## Data Flow Example

### Input
```
"You are Sheldon Cooper. Always use Bazinga!"
```

### Layer 1 Output (Canonical)
```json
{
  "type": "prompt",
  "roles": ["sheldon"],
  "constraints": ["strict_behavior", "catchphrase_required"],
  "goal": "roleplay",
  "interaction_pattern": "unstructured",
  "metadata": {"length": "short", "complexity": "simple"}
}
```

### Layer 2 Output (Fingerprint)
```json
{
  "role_count": 1,
  "constraint_count": 2,
  "constraint_density": 1.0,
  "complexity_score": 4.5,
  "has_roles": true,
  "has_constraints": true
}
```

### Layer 3 Output (Tags)
```json
{
  "primary_tags": ["roleplay", "persona_lock"],
  "secondary_tags": ["character_consistency"],
  "confidence": {
    "roleplay": 0.95,
    "persona_lock": 0.90
  }
}
```

### Layer 4 Output (Similarity Report)
```json
{
  "similarity_score": 0.983,
  "breakdown": {
    "structural": 0.944,
    "tag_overlap": 1.000,
    "pattern_match": 1.000
  },
  "explanation": {
    "matched_tags": ["roleplay", "persona_lock"],
    "key_similarities": ["Both define roles/personas"]
  },
  "verdict": "high_similarity"
}
```

## Performance Characteristics

- **Speed**: >100 prompts/second (without embeddings)
- **Memory**: Minimal (no model loading for core)
- **Accuracy**: >85% on test datasets
- **Explainability**: 100% (every decision is traceable)

## Extension Points

### Adding Custom Intent Tags
Edit `vocabularies/intent_tags.json`:
```json
{
  "your_custom_tag": {
    "description": "Your tag description",
    "rules": {
      "required": ["field_name"],
      "keywords": ["keyword1", "keyword2"]
    }
  }
}
```

### Adding Custom Patterns
Edit `vocabularies/patterns.json`:
```json
{
  "your_pattern": {
    "description": "Pattern description",
    "indicators": ["indicator1", "indicator2"]
  }
}
```

### Extending Layers
Each layer is a separate Python class that can be:
- Subclassed for custom behavior
- Replaced entirely with alternative implementations
- Extended with additional methods

## Future Enhancements

1. **Version Lineage Tracking**: Track how prompts evolve over time
2. **Bias Fingerprinting**: Detect structural biases
3. **Prompt Evolution Graphs**: Visualize prompt relationships
4. **IDE Integrations**: Real-time duplicate detection in editors
5. **API Server**: RESTful API for web integration
