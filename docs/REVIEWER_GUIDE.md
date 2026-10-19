# Five-minute reviewer walkthrough — RubricLedger

1. Read the standalone source: [`contracts/rubric_ledger.py`](../contracts/rubric_ledger.py).
2. Read [threat model](THREAT_MODEL.md), including role, model and integration limitations.
3. Run `python -m pytest tests/offline -q`: SDK-stub logic only, no consensus.
4. Run `python -m pytest tests/direct -q` with dependencies installed: real GenLayer Direct Mode with fixed LLM mocks; inspect the validator disagreement and confidence-boundary tests.
5. Run `genvm-lint check contracts/rubric_ledger.py`.
6. Only with deployment approval, manually trigger `.github/workflows/studionet.yml`. Compare live run contract-address / transactions / readbacks with SHA-256 in [proof status](PROOF_STATUS.md).
7. Submissions must not claim mainnet behavior, guaranteed validator model accuracy, unobserved transactions or point awards.

This project is materially separate from other user repositories and contains no frontend or token escrow.
