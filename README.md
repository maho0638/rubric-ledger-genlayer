# RubricLedger — Frozen Multicriterion Acceptance for GenLayer

**One reusable Intelligent Contract for AI-agent and freelance task acceptance.** A requester creates a work order with 1–4 immutable natural-language criteria and names the designated worker. The worker submits text evidence; GenLayer validators independently evaluate **every criterion** as `PASS`, `FAIL`, or `UNCLEAR`. Only an **all-PASS** consensus verdict becomes `ACCEPTED`.

One failed or unclear first submission creates `REVISION_ALLOWED`. The worker may submit a second attempt. If the second attempt still fails, the work order ends as `NOT_ACCEPTED`; accepted and earlier revision receipts remain immutable. A requester may cancel an unfinished order. No token escrow or transfer occurs.

## Why GenLayer?

Accepting natural-language tasks requires semantic judgment; a normal EVM contract can enforce the iteration cap and ownership but cannot decide whether a written deliverable satisfies a human requirement. Every validator reruns the bounded rubric evaluation and compares the **full normalized criterion vector**, not an approximate numerical score. Confidence below 80 or malformed/short arrays becomes `UNCLEAR` for all criteria; no acceptance is inferred. Storage updates happen only after the nondeterministic consensus result is returned.

## Example

Frozen rubric (order does not affect the SHA-256 digest):

```text
docs|Includes an installation guide
tests|Includes two reproducible test scenarios
```

- Requester calls `create_order("sdk-guide", worker_addr, "SDK guide", rubric)`.
- Worker calls `submit("try-one", "sdk-guide", "Work evidence ...")`.
- Read `get_receipt("try-one")`, `get_order("sdk-guide")`, and `is_accepted("sdk-guide")`.
- `PASS|UNCLEAR` means **not accepted** and allows exactly one revision; `PASS|PASS` means `ACCEPTED`.

The contract stores hashed submission content, canonical frozen criteria, criterion outcomes, and append-only receipts. It **does not** fetch links, prove that user-supplied evidence is authentic, judge private files, transfer payment, or automatically verify code. This is an explicit caller-trust boundary.

## Reproduce

```bash
pip install -r requirements.txt
python -m pytest tests/offline -q      # SDK stub only, NOT network proof
python -m pytest tests/direct -q       # GenLayer Direct Mode, mocked LLM
 genvm-lint check contracts/rubric_ledger.py
```

CI: `.github/workflows/ci.yml`. Opt-in real Studionet check: `.github/workflows/studionet.yml`. Verified results and their precise limits belong in `docs/PROOF_STATUS.md`. The portal draft is `SUBMISSION_DRAFT.md`.

## Verified GitHub CI (19 October 2026)

- 25/25 offline SDK-stub logic tests passed (not on-chain proof).
- 25/25 GenLayer Direct Mode tests passed with validator re-execution mocks.
- GenVM linter: 3/3 checks passed.
- [GitHub Actions run](https://github.com/maho0638/rubric-ledger-genlayer/actions/runs/39205927038).
- Source SHA-256: `11e8f3b4916dfa212912d0f363f8ca77de4a410efcca2fed5b73ebd151b9680e`.
- **No live Studionet run or Portal submission is claimed.**
