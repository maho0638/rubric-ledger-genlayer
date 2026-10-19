"""Opt-in network proof. Only run after user authorizes testnet transactions."""
import hashlib
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


def pick(result,name):
    return result.get(name) if isinstance(result,dict) else getattr(result,name)


@pytest.mark.integration
def test_network_work_order_lifecycle(default_account):
    c=get_contract_factory("RubricLedger").deploy(account=default_account,consensus_max_rotations=4)
    print("RUBRIC_ADDRESS="+str(c.address),flush=True)
    criteria="docs|The deliverable includes a clear setup guide\ntests|The deliverable includes two reproducible test scenarios"
    tx=c.create_order(args=["demo-task",str(default_account.address),"A mini SDK guide",criteria]).transact(wait_interval=10000,wait_retries=50)
    assert tx_execution_succeeded(tx)
    print("CREATE_TX="+str(tx.get("hash","")),flush=True)
    order=c.get_order(args=["demo-task"]).call()
    assert str(pick(order,"criteria_hash"))==hashlib.sha256(str(pick(order,"criteria")).encode()).hexdigest()

    evidence="Setup guide: install SDK then configure TEST_RPC. Two tests: (1) register a new user and read it back; (2) reject duplicate registration and assert failure."
    tx=c.submit(args=["attempt-one","demo-task",evidence]).transact(consensus_max_rotations=4,wait_interval=10000,wait_retries=80)
    assert tx_execution_succeeded(tx)
    print("JUDGE_TX="+str(tx.get("hash","")),flush=True)
    receipt=c.get_receipt(args=["attempt-one"]).call()
    assert str(pick(receipt,"verdict")) in ("ACCEPTED","REVISION_ALLOWED")
    assert str(pick(receipt,"evidence_hash"))==hashlib.sha256(evidence.encode()).hexdigest()
    labels=str(pick(receipt,"criterion_results")).split("|")
    assert len(labels)==2 and all(x in ("PASS","FAIL","UNCLEAR") for x in labels)
    print("RESULT="+str(pick(receipt,"verdict"))+"/"+"|".join(labels),flush=True)
