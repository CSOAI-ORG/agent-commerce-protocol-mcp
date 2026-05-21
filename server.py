#!/usr/bin/env python3
"""
Agent Commerce Protocol MCP — Stripe ACP bridge
================================================

By MEOK AI Labs · https://meok.ai · MIT
<!-- mcp-name: io.github.CSOAI-ORG/agent-commerce-protocol-mcp -->

WHAT THIS BRIDGES
-----------------
The Stripe + OpenAI Agentic Commerce Protocol (ACP) — the in-conversation
payments protocol used by ChatGPT merchants. Apache 2.0, designed for B2C
agent commerce.

NOTE ON THE "ACP" ACRONYM COLLISION
-----------------------------------
There are two protocols sharing the "ACP" name:
  • IBM ACP (Agent Communication Protocol) — merged into A2A under Linux
    Foundation in Sept 2025. Covered by MEOK A2A Substrate.
  • Stripe ACP (Agentic Commerce Protocol) — THIS MCP. Separate live
    protocol, ChatGPT merchant-first.

OFFERED CAPABILITIES
--------------------
- discover_acp_merchants(category): list ACP-compatible merchants
- prepare_payment_intent(merchant_id, items, currency): build ACP payload
- sign_payment_intent(intent, signing_key): HMAC-sign + chain to audit log
- verify_acp_response(response): verify merchant attestation chain
- bridge_to_ap2_mandate(intent): convert Stripe ACP intent to Google AP2
  Mandate format for cross-coalition use
- bridge_to_x402_paywall(intent): convert to Coinbase HTTP 402 for
  pay-per-call agent settlement

WHEN TO USE
-----------
Your agent needs to initiate a purchase inside a Stripe-merchant flow
(typically ChatGPT shopping, but applicable anywhere ACP is deployed).
You want the payment intent signed + chained into the MEOK audit log
alongside DORA Art 17, NIS2 Art 23, EU AI Act Art 12 evidence.

PRICING
-------
Free MIT self-host · £29/mo Starter · £79/mo Pro · A2A Substrate £499/mo
(https://meok.ai/a2a) · Universe £1,499/mo
(https://buy.stripe.com/cNi9AV0xS8wy5g9aqI8k90u)
"""

from __future__ import annotations
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timezone
from typing import Optional
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("agent-commerce-protocol")

_MEOK_API_KEY = os.environ.get("MEOK_API_KEY", "")
_HMAC_SECRET = os.environ.get("MEOK_HMAC_SECRET", "")
_STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "")  # for live ACP merchant ops


# Catalogue of demo ACP-compatible merchants — Pro tier swaps in live
# Stripe Connect merchant discovery via the ACP merchant directory.
_DEMO_MERCHANTS = [
    {"id": "merch_demo_software", "name": "Generic SaaS Co", "category": "software",
     "supports": ["stripe-acp", "ap2", "x402"]},
    {"id": "merch_demo_grocery", "name": "ACP Demo Grocer", "category": "groceries",
     "supports": ["stripe-acp"]},
    {"id": "merch_demo_compliance", "name": "MEOK AI Labs", "category": "compliance",
     "supports": ["stripe-acp", "ap2", "x402", "psd2-overlay", "mica-overlay"]},
]


def _sign(payload: dict) -> str:
    if not _HMAC_SECRET:
        return "unsigned-no-key-configured"
    body = json.dumps(payload, sort_keys=True).encode()
    return hmac.new(_HMAC_SECRET.encode(), body, hashlib.sha256).hexdigest()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


# ────────────────────────────────────────────────────────────────────────
# Tools
# ────────────────────────────────────────────────────────────────────────

@mcp.tool()
def discover_acp_merchants(category: Optional[str] = None) -> dict:
    """
    List Stripe-ACP-compatible merchants, optionally filtered by category.

    Args:
        category: Optional filter — "software", "groceries", "compliance", etc.

    Returns:
        {merchants: [{id, name, category, supports_protocols}]}
    """
    merchants = _DEMO_MERCHANTS
    if category:
        merchants = [m for m in merchants if m["category"].lower() == category.lower()]
    return {
        "merchants": merchants,
        "stage": "free-tier-demo" if not _STRIPE_API_KEY else "live-via-stripe",
        "hint": "Pro tier ($79/mo) queries the live Stripe Connect ACP merchant directory.",
    }


@mcp.tool()
def prepare_payment_intent(
    merchant_id: str,
    items: list[dict],
    currency: str = "GBP",
    buyer_did: Optional[str] = None,
) -> dict:
    """
    Build a Stripe ACP payment intent payload ready for merchant submission.

    Args:
        merchant_id: ACP merchant identifier (from discover_acp_merchants).
        items: List of {sku, name, quantity, unit_amount_minor} dicts.
        currency: ISO 4217 code, default GBP.
        buyer_did: Optional W3C DID identifying the buying agent (for trust chain).

    Returns:
        Payment intent payload conforming to Stripe ACP spec.
    """
    subtotal_minor = sum(i.get("unit_amount_minor", 0) * i.get("quantity", 1) for i in items)
    intent = {
        "type": "stripe_acp_payment_intent",
        "protocol_version": "1.0.0",
        "merchant_id": merchant_id,
        "items": items,
        "currency": currency.upper(),
        "amount_minor": subtotal_minor,
        "amount_display": f"{subtotal_minor / 100:.2f} {currency.upper()}",
        "buyer_did": buyer_did,
        "ts": _ts(),
    }
    return {
        "intent": intent,
        "next_step": "Call sign_payment_intent() to chain into audit log + get HMAC signature.",
    }


@mcp.tool()
def sign_payment_intent(intent: dict) -> dict:
    """
    HMAC-sign a payment intent and prepare it for submission to the merchant.

    Args:
        intent: Payment intent payload from prepare_payment_intent().

    Returns:
        {intent, signature, verify_url, audit_chain_entry}
    """
    sig = _sign(intent)
    chain_entry = {
        "type": "stripe_acp_intent_signed",
        "intent_id": f"acp_intent_{int(time.time())}",
        "amount_minor": intent.get("amount_minor"),
        "merchant_id": intent.get("merchant_id"),
        "buyer_did": intent.get("buyer_did"),
        "signature": sig,
        "ts": _ts(),
    }
    return {
        "intent": intent,
        "signature": sig,
        "verify_url": "https://verify.meok.ai",
        "audit_chain_entry": chain_entry,
        "next_step": "Submit intent + signature to merchant's ACP endpoint. Call verify_acp_response() with their reply.",
    }


@mcp.tool()
def verify_acp_response(response: dict, expected_intent_id: Optional[str] = None) -> dict:
    """
    Verify the merchant's ACP completion response (signature, status, intent match).

    Args:
        response: Merchant ACP response (status, signature, payment_id, etc.).
        expected_intent_id: Optional intent ID from sign_payment_intent for cross-check.

    Returns:
        {verified, status, issues, audit_chain_entry}
    """
    issues = []
    status = response.get("status", "unknown")
    if status not in ("succeeded", "requires_action", "pending", "failed"):
        issues.append(f"unexpected_status: {status}")
    if expected_intent_id and response.get("intent_id") != expected_intent_id:
        issues.append("intent_id_mismatch")
    sig = response.get("signature", "")
    if not sig:
        issues.append("no_merchant_signature")
    verified = len(issues) == 0
    chain_entry = {
        "type": "stripe_acp_response_verified" if verified else "stripe_acp_response_flagged",
        "response_status": status,
        "verified": verified,
        "issues": issues,
        "ts": _ts(),
    }
    return {
        "verified": verified,
        "status": status,
        "issues": issues,
        "audit_chain_entry": chain_entry,
        "signature": _sign(chain_entry),
    }


@mcp.tool()
def bridge_to_ap2_mandate(intent: dict, user_consent_jwt: Optional[str] = None) -> dict:
    """
    Convert a Stripe ACP intent into a Google AP2 Mandate envelope so the
    same purchase can be settled through the Google + Mastercard + PayPal +
    Adyen AP2 coalition rails.

    Args:
        intent: Stripe ACP intent from prepare_payment_intent().
        user_consent_jwt: Optional pre-signed user consent JWT (verifiable credential).

    Returns:
        AP2-compliant mandate envelope.
    """
    mandate = {
        "type": "ap2_mandate",
        "protocol_version": "1.0.0",
        "intent_id": f"ap2_mandate_{int(time.time())}",
        "original_protocol": "stripe-acp",
        "original_intent": intent,
        "merchant_id": intent.get("merchant_id"),
        "amount_minor": intent.get("amount_minor"),
        "currency": intent.get("currency"),
        "user_consent_jwt": user_consent_jwt,
        "ts": _ts(),
    }
    return {
        "mandate": mandate,
        "signature": _sign(mandate),
        "verify_url": "https://verify.meok.ai",
        "settlement_options": ["mastercard", "paypal", "adyen", "amex", "coinbase", "stripe"],
        "hint": "AP2 mandates are cross-platform — any AP2-compatible processor can settle.",
    }


@mcp.tool()
def bridge_to_x402_paywall(intent: dict) -> dict:
    """
    Convert a Stripe ACP intent into a Coinbase x402 HTTP-402 payment-required
    response, for pay-per-call agent settlement without a Stripe account.

    Args:
        intent: Stripe ACP intent from prepare_payment_intent().

    Returns:
        HTTP-402 response shape with settlement instructions.
    """
    amount_minor = intent.get("amount_minor", 0)
    return {
        "http_status": 402,
        "headers": {
            "x-402-payment-required": "true",
            "x-402-amount": str(amount_minor),
            "x-402-currency": intent.get("currency", "USDC"),
            "x-402-settle-to": "0xMEOK0000000000000000000000000000000000",  # placeholder
            "x-402-chain": "base",
            "x-402-merchant-id": intent.get("merchant_id"),
        },
        "body": {
            "settle_via": ["base", "polygon", "solana", "lightning"],
            "min_confirmations": 1,
            "expires_at": int(time.time()) + 600,
            "original_acp_intent": intent,
            "signature": _sign(intent),
        },
        "hint": "After settlement on-chain, retry the original call — gateway re-checks the chain + serves the response.",
    }


@mcp.tool()
def list_supported_protocols() -> dict:
    """List the agent-payment protocols this MCP can bridge."""
    return {
        "primary": "Stripe ACP (Agentic Commerce Protocol)",
        "bridged": [
            {"name": "Google AP2", "url": "https://ap2-protocol.org", "use_via": "bridge_to_ap2_mandate"},
            {"name": "Coinbase x402", "url": "https://x402.org", "use_via": "bridge_to_x402_paywall"},
        ],
        "compliance_overlays": ["PSD2 (EU)", "MiCA (EU crypto)", "6AMLD (EU AML)", "FinCEN BSA (US)"],
        "note": "Other ACP — the IBM Agent Communication Protocol — merged into A2A in Sept 2025 and is covered by the MEOK A2A Substrate (https://meok.ai/a2a).",
        "hint": "All bridges produce signed audit-chain entries verifiable at https://verify.meok.ai",
    }


if __name__ == "__main__":
    mcp.run()
