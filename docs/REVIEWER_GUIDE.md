# Five-minute reviewer walkthrough — RubricLedger

1. Read the standalone source: [`contracts/rubric_ledger.py`](../contracts/rubric_ledger.py).
2. Read [threat model](THREAT_MODEL.md), including role, model and integration limitations.
3. Run `python -m pytest tests/offline -q`: SDK-stub logic only, no consensus.
4. Run `python -m pytest tests/direct -q` with dependencies installed: real GenLayer Direct Mode with fixed LLM mocks; inspect the validator disagreement and confidence-boundary tests.
5. Run `genvm-lint check contracts/rubric_ledger.py`.
6. Only with deployment approval, manually trigger `.github/workflows/studionet.yml`. Compare live run contract-address / transactions / readbacks with SHA-256 in [proof status](PROOF_STATUS.md).
7. Submissions must not claim mainnet behavior, guaranteed validator model accuracy, unobserved transactions or point awards.

This project is materially separate from other user repositories and contains no frontend or token escrow.

## Verified live execution

# Verified Studionet proof — RubricLedger

- **State**: live Studionet integration 1/1 passed on 19 October 2026.
- **CI / offline**: 25/25 SDK stub tests, 25/25 GenLayer Direct Mode tests, 3/3 GenVM lint: https://github.com/maho0638/rubric-ledger-genlayer/actions/runs/39205927038
- **Live**: https://github.com/maho0638/rubric-ledger-genlayer/actions/runs/39207919088
- **Contract source**: `contracts/rubric_ledger.py`; SHA-256 `11e8f3b4916dfa212912d0f363f8ca77de4a410efcca2fed5b73ebd151b9680e` matched both CI and live test logs.
- **Contract address**: `0x2ACc9B1b803649DC9fa0EC38A4f15896923e7d68`
- **Explorer**: https://explorer-studio.genlayer.com/address/0x2ACc9B1b803649DC9fa0EC38A4f15896923e7d68
- **Observed on-chain result**: `ACCEPTED/PASS|PASS`
- **Observed lifecycle**: Registered a frozen two-criterion work order and obtained a live consensus-backed ACCEPTED decision with PASS/PASS; hash and readback checks passed.

- **CREATE_TX**: `0x44de4dba68e0155aaaa69b817cc77d9dfd86b3cfbaee0173c2aa5bef6e4b7451`
- **JUDGE_TX**: `0xa629eee057301ddd8ab8c6abf6915fc1827406102eb0b869eb78e49d0a898816`

## Limits
This proves only the observed integration lifecycle and readback, not a formal security audit, perfect model accuracy, or all possible validator rotations. Direct Mode separately tests edge cases and disagreement. No native-GEN escrow or user wallet custody is part of these contracts. No Portal submission or rating is claimed.
