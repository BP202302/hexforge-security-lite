# Validation and precision

HexForge Lite uses validators after module execution. This keeps modules simple while allowing the pipeline to normalize severity and confidence.

## Precision safeguards

- Wildcard CORS with absent credentials is low/review, not high.
- HSTS duplicates are collapsed.
- Discovery files are informational by default.
- Missing headers are confirmed observations, not proof of exploitability.
- Token-like strings require manual review unless additional context exists.

## Finding categories

- `Confirmed`: direct evidence supports a meaningful security issue.
- `Review`: configuration needs human context.
- `Informational`: useful observation, not a vulnerability by itself.
