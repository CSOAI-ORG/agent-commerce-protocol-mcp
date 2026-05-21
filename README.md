# Agent Commerce Protocol MCP

> ## 🧱 Part of the MEOK A2A Substrate
>
> All 12 A2A primitives + Stripe ACP bridge as one signed pipeline for
> **£499/mo**. See [meok.ai/a2a](https://meok.ai/a2a).

# Bridges Stripe ACP + Google AP2 + Coinbase x402

<!-- mcp-name: io.github.CSOAI-ORG/agent-commerce-protocol-mcp -->

[![PyPI](https://img.shields.io/pypi/v/agent-commerce-protocol-mcp)](https://pypi.org/project/agent-commerce-protocol-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP Registry](https://img.shields.io/badge/MCP_Registry-Published-green)](https://registry.modelcontextprotocol.io)

## The "ACP" name collision

There are two protocols called "ACP" — they do different things:

| | IBM ACP | **Stripe ACP** |
|---|---|---|
| **Full name** | Agent Communication Protocol | Agentic Commerce Protocol |
| **Owner** | IBM Research (was) | Stripe + OpenAI |
| **Status** | Merged into A2A under Linux Foundation Sept 2025 | LIVE — Apache 2.0 |
| **What it does** | Agent-to-agent messaging | In-conversation payments |
| **Where you hit it** | A2A protocol stack | ChatGPT merchant flows |
| **MEOK coverage** | A2A Substrate (12 MCPs) | **THIS MCP** |

This MCP is **the Stripe ACP one** — agent payments inside ChatGPT-style flows.

## What this gives you

The **only MCP that bridges all 3 live agent-payment protocols**:

- **Stripe ACP** — primary, for ChatGPT merchant flows
- **Google AP2** — bridged, for the 60-org Mastercard/PayPal/Adyen coalition
- **Coinbase x402** — bridged, for HTTP-402 pay-per-call without a Stripe account

Plus EU compliance overlays automatically applied to every transaction: **PSD2** (EU), **MiCA** (EU crypto), **6AMLD** (EU AML), **FinCEN BSA** (US).

Every payment intent + verification signs into the MEOK audit chain at `verify.meok.ai`.

## Tools

| Tool | Purpose |
|---|---|
| `discover_acp_merchants(category?)` | List Stripe-ACP-compatible merchants |
| `prepare_payment_intent(merchant_id, items, currency)` | Build Stripe ACP intent |
| `sign_payment_intent(intent)` | HMAC-sign + chain into audit log |
| `verify_acp_response(response, expected_intent_id?)` | Verify merchant attestation |
| `bridge_to_ap2_mandate(intent, user_consent_jwt?)` | Convert to Google AP2 mandate |
| `bridge_to_x402_paywall(intent)` | Convert to Coinbase HTTP 402 |
| `list_supported_protocols()` | Capability discovery |

## Quick install

```bash
uvx agent-commerce-protocol-mcp
pip install agent-commerce-protocol-mcp
npx @meok-ai/agent-commerce-protocol-mcp
```

Claude Desktop / Cursor / Windsurf MCP config:

```json
{
  "mcpServers": {
    "agent-commerce-protocol": {
      "command": "uvx",
      "args": ["agent-commerce-protocol-mcp"]
    }
  }
}
```

## Why this matters for £-revenue

Stripe ACP is the protocol Stripe + OpenAI are pushing through ChatGPT's shopping interface. Every ChatGPT merchant gets Stripe ACP free with their OpenAI integration. If your agent participates in ChatGPT commerce (or any merchant flow built on Stripe Connect ACP), you need this MCP to:

1. **Initiate signed payment intents** with audit-trail evidence for EU AI Act Article 12 + DORA Article 17
2. **Bridge to AP2 mandates** if the merchant runs on Mastercard/PayPal/Adyen rails instead of pure Stripe
3. **Bridge to x402** if your agent settles micropayments on-chain (Base / Polygon / Solana / Lightning)

## Sister MCPs

Part of the MEOK **A2A** pack:

- **agent-commerce-payments-mcp** → invoicing + escrow + AML/KYC
- **agent-prompt-injection-firewall-mcp** → scan payment prompts for injection
- **agent-policy-enforcement-mcp** → gate which agents can spend
- **agent-rate-limiter-mcp** → cap call volume per session
- **agent-audit-logger-mcp** → hash-chained log of every payment intent
- **agent-identity-trust-mcp** → buyer DID resolution

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Protocol coverage + Universal PAYG

| Option | Price | Best for |
|---|---|---|
| Self-host (this MCP) | £0 — MIT | Devs |
| This MCP Starter | £29/mo | One-MCP teams |
| Universal PAYG | £29/mo + £0.0002/call | Spiky usage |
| A2A Substrate | £499/mo | All 13 A2A MCPs |
| Universe | £1,499/mo | All 48 MEOK MCPs |

Buy: https://meok.ai/a2a

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677). Founder: [Nicholas Templeman](mailto:nicholas@meok.ai).
