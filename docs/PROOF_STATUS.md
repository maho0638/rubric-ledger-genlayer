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
