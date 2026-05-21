"""Smoke tests for agent-commerce-protocol-mcp."""
import sys, os, inspect, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    discover_acp_merchants,
    prepare_payment_intent,
    sign_payment_intent,
    verify_acp_response,
    bridge_to_ap2_mandate,
    bridge_to_x402_paywall,
    list_supported_protocols,
)


def test_discover_all_merchants():
    r = discover_acp_merchants()
    assert len(r["merchants"]) >= 3
    assert all("supports" in m for m in r["merchants"])


def test_discover_filtered():
    r = discover_acp_merchants(category="compliance")
    assert all(m["category"] == "compliance" for m in r["merchants"])


def test_prepare_intent_sums_correctly():
    items = [
        {"sku": "A1", "name": "thing 1", "quantity": 2, "unit_amount_minor": 1500},
        {"sku": "B1", "name": "thing 2", "quantity": 1, "unit_amount_minor": 4900},
    ]
    r = prepare_payment_intent("merch_demo_software", items, "GBP", buyer_did="did:agent:test")
    assert r["intent"]["amount_minor"] == 1500 * 2 + 4900
    assert r["intent"]["currency"] == "GBP"
    assert r["intent"]["buyer_did"] == "did:agent:test"


def test_sign_intent_returns_chain_entry():
    intent = prepare_payment_intent("merch_demo_software", [{"sku": "x", "quantity": 1, "unit_amount_minor": 100}])["intent"]
    r = sign_payment_intent(intent)
    assert "signature" in r and len(r["signature"]) > 5
    assert r["audit_chain_entry"]["type"] == "stripe_acp_intent_signed"


def test_verify_response_flags_issues():
    bad_response = {"status": "weird", "intent_id": "X"}
    r = verify_acp_response(bad_response, expected_intent_id="Y")
    assert r["verified"] is False
    assert any("status" in i or "mismatch" in i for i in r["issues"])


def test_verify_response_passes_clean():
    good_response = {"status": "succeeded", "intent_id": "abc", "signature": "deadbeef"}
    r = verify_acp_response(good_response, expected_intent_id="abc")
    assert r["verified"] is True
    assert r["issues"] == []


def test_bridge_to_ap2_preserves_amount():
    intent = prepare_payment_intent("m1", [{"sku": "x", "quantity": 1, "unit_amount_minor": 999}], "EUR")["intent"]
    r = bridge_to_ap2_mandate(intent, user_consent_jwt="jwt.placeholder")
    assert r["mandate"]["amount_minor"] == 999
    assert r["mandate"]["currency"] == "EUR"
    assert "mastercard" in r["settlement_options"]


def test_bridge_to_x402_returns_402():
    intent = prepare_payment_intent("m1", [{"sku": "x", "quantity": 1, "unit_amount_minor": 100}], "USD")["intent"]
    r = bridge_to_x402_paywall(intent)
    assert r["http_status"] == 402
    assert "x-402-amount" in r["headers"]
    assert r["body"]["expires_at"] > 0


def test_list_supported_protocols():
    r = list_supported_protocols()
    assert "Stripe ACP" in r["primary"]
    assert len(r["bridged"]) >= 2
    assert "IBM" in r["note"]  # acknowledges name collision


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    passed = failed = 0
    for fn in fns:
        try:
            fn()
            print(f"✓ {fn.__name__}")
            passed += 1
        except Exception as e:
            print(f"✗ {fn.__name__}: {type(e).__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
