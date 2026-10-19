"""Real GenLayer Direct Mode with validator-decisive vector tests."""
import hashlib
import json
import pytest

CRITERIA="documentation|Includes installation steps\ntests|Includes reproducible tests"


def mk(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=direct_deploy("contracts/rubric_ledger.py")
    direct_vm.sender=direct_alice
    c.create_order("work1","0x" + direct_bob.hex(),"SDK documentation",CRITERIA)
    direct_vm.sender=direct_bob
    return c


def mock(direct_vm,labels=("PASS","PASS"),confidence=90):
    direct_vm.clear_mocks()
    direct_vm.mock_llm(r"(?s).*RubricLedger evaluates written deliverables.*", json.dumps({"results":list(labels),"confidence":confidence}))


def test_first_accepts_and_immutable(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm)
    c.submit("attempt1","work1","Installation guide and tests attached")
    assert c.get_receipt("attempt1").verdict=="ACCEPTED"
    assert c.is_accepted("work1") is True
    assert int(c.get_order("work1").attempts)==1
    assert direct_vm.run_validator() is True


@pytest.mark.parametrize("labels",[("PASS","FAIL"),("FAIL","PASS"),("UNCLEAR","PASS")])
def test_revision_allowed(labels,direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm,labels)
    c.submit("attempt1","work1","Not complete")
    assert c.get_receipt("attempt1").verdict=="REVISION_ALLOWED"
    assert not c.is_accepted("work1")


def test_revision_then_accept(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm,("FAIL","PASS"))
    c.submit("a1","work1","Only tests")
    mock(direct_vm,("PASS","PASS"))
    c.submit("a2","work1","Added instructions and tests")
    assert c.is_accepted("work1")
    assert int(c.get_order("work1").attempts)==2
    assert c.get_receipt("a1").verdict=="REVISION_ALLOWED"
    assert c.get_receipt("a2").verdict=="ACCEPTED"


def test_second_failure_is_final(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm,("FAIL","FAIL"))
    c.submit("a1","work1","Incomplete")
    c.submit("a2","work1","Still incomplete")
    assert c.get_order("work1").state=="NOT_ACCEPTED"
    with direct_vm.expect_revert("Order closed"):
        c.submit("a3","work1","Try again",)


@pytest.mark.parametrize("confidence",[0,55,79,101])
def test_low_confidence_cannot_accept(confidence,direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm,("PASS","PASS"),confidence)
    c.submit("a1","work1","Looks complete")
    assert c.get_receipt("a1").criterion_results=="UNCLEAR|UNCLEAR"
    assert not c.is_accepted("work1")


def test_malformed_length_fails_closed(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm,("PASS",),92)
    c.submit("a1","work1","Evidence")
    assert c.get_receipt("a1").criterion_results=="UNCLEAR|UNCLEAR"


def test_validator_decisive_disagreement(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm,("PASS","PASS"),90)
    c.submit("a1","work1","Evidence")
    mock(direct_vm,("PASS","FAIL"),90)
    assert direct_vm.run_validator() is False


def test_validator_confidence_crossing_rejected(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm,("PASS","PASS"),90)
    c.submit("a1","work1","Evidence")
    mock(direct_vm,("PASS","PASS"),65)
    assert direct_vm.run_validator() is False


def test_validator_safe_drift(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm,("PASS","PASS"),90)
    c.submit("a1","work1","Evidence")
    mock(direct_vm,("PASS","PASS"),84)
    assert direct_vm.run_validator() is True


def test_worker_only(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    direct_vm.sender=direct_alice
    with direct_vm.expect_revert("Only assigned worker"):
        c.submit("a1","work1","Evidence")


def test_cancel_only_requester(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    with direct_vm.expect_revert("Only requester"):
        c.cancel_order("work1")
    direct_vm.sender=direct_alice
    c.cancel_order("work1")
    assert c.get_order("work1").state=="CANCELLED"
    direct_vm.sender=direct_bob
    with direct_vm.expect_revert("Order closed"):
        c.submit("a1","work1","Evidence")


def test_immutable_hashes_and_sorted_criteria(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    order=c.get_order("work1")
    assert order.criteria.startswith("documentation|")
    assert order.criteria_hash==hashlib.sha256(order.criteria.encode()).hexdigest()
    mock(direct_vm)
    c.submit("a1","work1","Evidence")
    assert c.get_receipt("a1").criteria_hash==order.criteria_hash
    with direct_vm.expect_revert("Duplicate receipt"):
        c.submit("a1","work1","Other evidence")


@pytest.mark.parametrize("criteria",["", "missing separator", "a|", "a|ok\na|duplicate", "a|ok\n\n", "a|"+"x"*241, "a|valid\nb|valid\nc|valid\nd|valid\ne|valid"])
def test_invalid_criteria(criteria,direct_vm,direct_deploy,direct_alice,direct_bob):
    c=direct_deploy("contracts/rubric_ledger.py")
    direct_vm.sender=direct_alice
    with direct_vm.expect_revert():
        c.create_order("w1","0x" + direct_bob.hex(),"Title",criteria)

def test_identical_revision_rejected(direct_vm,direct_deploy,direct_alice,direct_bob):
    c=mk(direct_vm,direct_deploy,direct_alice,direct_bob)
    mock(direct_vm,("FAIL","PASS"))
    c.submit("a1","work1","Same evidence")
    with direct_vm.expect_revert("Revision must contain changed evidence"):
        c.submit("a2","work1","Same evidence")
