## Summary

<!-- What does this change and why? -->

## Checklist

- [ ] `ruff check .` passes
- [ ] `mypy` passes
- [ ] `lint-imports` passes (Clean Architecture dependency contract)
- [ ] `bash scripts/ip_grep.sh` passes
- [ ] `pytest` passes
- [ ] `python eval/SPEC-2026-0701/gate.py` passes (AC-1..AC-15)
- [ ] New behavior is covered by tests
- [ ] The domain core stays pure; scoring stays deterministic; narration does not score
