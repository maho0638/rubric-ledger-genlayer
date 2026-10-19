"""SDK-free logic simulation; this is not GenVM or live network proof."""
import importlib.util
import pathlib
import sys
import types
import hashlib
import pytest

ROOT=pathlib.Path(__file__).resolve().parents[2]
CRITERIA="docs|Has clear installation steps\ntests|Includes reproducible tests"

@pytest.fixture()
def env():
    sdk=types.ModuleType("genlayer")
    class UserError(Exception):pass
    class Return:
        def __init__(self,calldata):self.calldata=calldata
    class Contract:pass
    vm=types.SimpleNamespace(UserError=UserError,Return=Return)
    gl=types.SimpleNamespace(Contract=Contract,public=types.SimpleNamespace(write=lambda x:x,view=lambda x:x),vm=vm,
        message=types.SimpleNamespace(sender_address="OWNER"),nondet=types.SimpleNamespace(exec_prompt=lambda *a,**k:{"results":["PASS","PASS"],"confidence":90}))
    vm.run_nondet_unsafe=lambda leader,validator:leader()
    sdk.gl=gl;sdk.dataclass=__import__("dataclasses").dataclass;sdk.allow_storage=lambda x:x
    sdk.TreeMap=dict;sdk.Address=str;sdk.u256=int
    sys.modules["genlayer"]=sdk
    try:
        spec=importlib.util.spec_from_file_location("test_rubric_contract",ROOT/"contracts"/"rubric_ledger.py")
        mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
        c=mod.RubricLedger();c.orders={};c.receipts={}
        c.create_order("job1","WORKER","Write documentation",CRITERIA)
        gl.message.sender_address="WORKER"
        yield mod,c,gl
    finally:
        sys.modules.pop("genlayer",None);sys.modules.pop("test_rubric_contract",None)

def mock(env,labels=("PASS","PASS"),confidence=91):
    _mod,_c,gl=env
    gl.nondet.exec_prompt=lambda *_a,**_k:{"results":list(labels),"confidence":confidence}

def test_accepts_and_hashes(env):
    _,c,_=env;mock(env)
    c.submit("a1","job1","Installation guide with all tests")
    assert c.is_accepted("job1")
    assert c.get_receipt("a1").verdict=="ACCEPTED"
    assert c.get_receipt("a1").evidence_hash==hashlib.sha256(b"Installation guide with all tests").hexdigest()

@pytest.mark.parametrize("labels",[("FAIL","PASS"),("PASS","FAIL"),("UNCLEAR","PASS"),("UNCLEAR","UNCLEAR")])
def test_revision_allowed(env,labels):
    _,c,_=env;mock(env,labels)
    c.submit("a1","job1","Incomplete")
    assert c.get_receipt("a1").verdict=="REVISION_ALLOWED"
    assert not c.is_accepted("job1")


def test_revision_success_preserves_history(env):
    _,c,_=env;mock(env,("FAIL","PASS"))
    c.submit("a1","job1","Missing docs")
    mock(env,("PASS","PASS"))
    c.submit("a2","job1","Now with docs and tests")
    assert c.get_receipt("a1").criterion_results=="FAIL|PASS"
    assert c.get_receipt("a2").criterion_results=="PASS|PASS"
    assert c.is_accepted("job1")
    assert c.get_order("job1").attempts==2


def test_second_failed_attempt_terminal(env):
    mod,c,_=env;mock(env,("FAIL","PASS"))
    c.submit("a1","job1","Missing docs")
    c.submit("a2","job1","Missing docs again")
    assert c.get_receipt("a2").verdict=="NOT_ACCEPTED"
    with pytest.raises(mod.gl.vm.UserError,match="Order closed"):
        c.submit("a3","job1","Late docs")

@pytest.mark.parametrize("confidence",[0,50,79,101])
def test_threshold_fails_closed(env,confidence):
    _,c,_=env;mock(env,("PASS","PASS"),confidence)
    c.submit("a1","job1","Looks complete")
    assert c.get_receipt("a1").criterion_results=="UNCLEAR|UNCLEAR"
    assert not c.is_accepted("job1")


def test_duplicate_receipt(env):
    mod,c,_=env;mock(env)
    c.submit("a1","job1","Complete")
    with pytest.raises(mod.gl.vm.UserError,match="Duplicate receipt"):
        c.submit("a1","job1","Changed")


def test_cancel_auth_and_state(env):
    mod,c,gl=env
    with pytest.raises(mod.gl.vm.UserError,match="Only requester"):
        c.cancel_order("job1")
    gl.message.sender_address="OWNER"
    c.cancel_order("job1")
    gl.message.sender_address="WORKER"
    with pytest.raises(mod.gl.vm.UserError,match="Order closed"):
        c.submit("a1","job1","Complete")


def test_worker_auth(env):
    mod,c,gl=env
    gl.message.sender_address="OTHER"
    with pytest.raises(mod.gl.vm.UserError,match="Only assigned worker"):
        c.submit("a1","job1","Complete")


def test_criteria_integrity(env):
    mod,c,gl=env
    order=c.get_order("job1")
    assert order.criteria_hash==hashlib.sha256(order.criteria.encode()).hexdigest()
    gl.message.sender_address="OWNER"
    with pytest.raises(mod.gl.vm.UserError,match="Duplicate order"):
        c.create_order("job1","WORKER","Other",CRITERIA)

@pytest.mark.parametrize("criteria",["", "a", "a|", "a|v\na|w", "a|ok\n\n", "a|"+"x"*241, "a|1\nb|2\nc|3\nd|4\ne|5"])
def test_bad_criteria(env,criteria):
    mod,c,gl=env
    gl.message.sender_address="OWNER"
    with pytest.raises(mod.gl.vm.UserError):
        c.create_order("different","WORKER","Title",criteria)


def test_validator_flip_and_threshold_crossing(env):
    mod,c,gl=env
    captured={}
    def run(leader,validator):
        result=leader();captured["validator"]=validator;captured["result"]=result;return result
    gl.vm.run_nondet_unsafe=run
    mock(env,("PASS","PASS"),95)
    c.submit("a1","job1","Complete")
    assert captured["validator"](mod.gl.vm.Return(captured["result"]))
    mock(env,("PASS","FAIL"),95)
    assert not captured["validator"](mod.gl.vm.Return(captured["result"]))
    mock(env,("PASS","PASS"),70)
    assert not captured["validator"](mod.gl.vm.Return(captured["result"]))


def test_validator_accepts_nondecisive_confidence_drift(env):
    mod,c,gl=env
    captured={}
    def run(leader,validator):
        result=leader();captured["validator"]=validator;captured["result"]=result;return result
    gl.vm.run_nondet_unsafe=run
    mock(env,("PASS","PASS"),95)
    c.submit("a1","job1","Complete")
    mock(env,("PASS","PASS"),85)
    assert captured["validator"](mod.gl.vm.Return(captured["result"]))

def test_identical_revision_is_rejected(env):
    mod,c,_=env;mock(env,("FAIL","PASS"))
    c.submit("a1","job1","Incomplete work")
    with pytest.raises(mod.gl.vm.UserError,match="Revision must contain changed evidence"):
        c.submit("a2","job1","Incomplete work")
    assert int(c.get_order("job1").attempts)==1
