# Portal draft — Intelligent Contracts (NOT SUBMITTED)

**Title:** RubricLedger — Multicriterion AI Deliverable Verification and Revision Receipts

**Category:** Developer / Intelligent Contracts

**Pitch:** RubricLedger records a work order with frozen natural-language acceptance requirements and a designated worker. On evidence submission, independent GenLayer validators assess every criterion separately as PASS / FAIL / UNCLEAR, then compare the exact decisive label vector. Invalid, ambiguous or below-threshold outputs become UNCLEAR; only unanimous normalized PASS across all criteria can lead to ACCEPTED. Deterministic state rules permit exactly one re-submission after a failed first attempt and preserve both hash-bound results in an immutable review history. Requester-only cancellation and worker-only submission prevent unauthorized transitions. Use cases: small AI-agent tasks, freelance deliverables, OSS bounties, editorial checklists. No native-GEN escrow, automatic transfer, third-party authenticity proof, or claims of formal correctness.

**Evidence:** Link source, passing GenLayer Direct Mode tests, GenVM linter, real Studionet contract and transaction records **only after successful runs**. See `docs/PROOF_STATUS.md`.

## Verified evidence (19 October 2026)
- Source: https://github.com/maho0638/rubric-ledger-genlayer
- Offline 25/25, Direct Mode 25/25, GenVM lint 3/3: https://github.com/maho0638/rubric-ledger-genlayer/actions/runs/39205927038
- Real Studionet 2-transaction lifecycle 1/1 passed: https://github.com/maho0638/rubric-ledger-genlayer/actions/runs/39207919088
- GenLayer Explorer contract: https://explorer-studio.genlayer.com/address/0x2ACc9B1b803649DC9fa0EC38A4f15896923e7d68
- Full transaction hashes and observed results: https://github.com/maho0638/rubric-ledger-genlayer/blob/main/docs/PROOF_MANIFEST.json
- Reproduction: https://github.com/maho0638/rubric-ledger-genlayer/blob/main/docs/REVIEWER_GUIDE.md
- Outcome: `ACCEPTED/PASS|PASS`. Registered a frozen two-criterion work order and obtained a live consensus-backed ACCEPTED decision with PASS/PASS; hash and readback checks passed.
