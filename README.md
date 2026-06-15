<!-- mcp-name: io.github.CSOAI-ORG/agent-commerce-protocol-mcp -->
[![MCP Scorecard: 90/100](https://img.shields.io/badge/proofof.ai-90%2F100-5b21b6)](https://proofof.ai/scorecard/agent-commerce-protocol-mcp.html)

mcp-name: io.github.CSOAI-ORG/agent-commerce-protocol-mcp

# Agent Commerce Protocol MCP

[![MEOK AI Labs](https://img.shields.io/badge/MEOK-AI%20Labs-667eea)](https://meok.ai)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Compliant-22c55e)](https://councilof.ai)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Install-3775a9)](https://pypi.org/project/agent_commerce_protocol_mcp/)

>   🧱 Part of the MEOK A2A Substrate

  🧱 Part of the MEOK A2A Substrate

---

## 🚀 Quick Start

```bash
# Install via pip
pip install agent_commerce_protocol_mcp

# Or install via Smithery
npx -y @smithery/cli@latest install agent-commerce-protocol-mcp --client claude
```

## ✨ Features

- Product catalog management
- Cart & checkout
- Stripe integration
- x402 protocol support
- Multi-currency

## 📖 Documentation

- [Full Documentation](https://docs.meok.ai/agent-commerce-protocol-mcp)
- [API Reference](https://api.meok.ai)
- [EU AI Act Compliance Guide](https://councilof.ai/compliance)

## 🛡️ Compliance

This MCP server is built with **EU AI Act compliance** built-in:

- ✅ Article 9 — Risk Management System
- ✅ Article 13 — Transparency & Instructions for Use
- ✅ Article 15 — Bias Detection & Testing
- ✅ Article 26 — FRIA Support (where applicable)
- ✅ Article 50 — AI Content Watermarking (where applicable)

Need help getting compliant? **[Book a free 15-min diagnostic →](https://cal.com/csoai/august-audit)**

## 🏢 Enterprise

Need custom development, SLA guarantees, or white-label deployment?

- **Pro:** $99/mo — Full MCP suite + EU AI Act tracking
- **Enterprise:** $499/mo — Custom dev + SLA + Dedicated support

[View Pricing →](https://councilof.ai/pricing) | [Contact Sales →](mailto:sales@csoai.org)

## 🤝 Part of the MEOK Ecosystem

This server is part of the **[MEOK AI Labs](https://meok.ai)** ecosystem — 300+ MCP servers for sovereign AI governance.

| Domain | Purpose |
|--------|---------|
| [councilof.ai](https://councilof.ai) | EU AI Act compliance marketplace |
| [safetyof.ai](https://safetyof.ai) | AI safety & monitoring |
| [meok.ai](https://meok.ai) | Sovereign AI platform |
| [cobolbridge.ai](https://cobolbridge.ai) | Legacy modernization |

## 📜 License

MIT © [CSOAI-ORG](https://github.com/CSOAI-ORG)

---

<p align="center">
  <sub>Built with 💜 by <a href="https://meok.ai">MEOK AI Labs</a> · UK Companies House 16939677</sub>
</p>
MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677). Founder: [Nicholas Templeman](mailto:nicholas@meok.ai).

<!-- BUY-LADDER:START -->

## 💸 Try MEOK in 30 seconds — instant buy ladder

| Tier | Price | What you get | Stripe |
|---|---|---|---|
| Smoke test | **£1** | Signed sample MCP-Hardening report + Article 50 PDF | <https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t> |
| Quick Kit | **£9** | EU AI Act Article 50 implementation guide (C2PA + EU-Icon) | <https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t> |
| Founder Call | **£29** | 30-min 1-on-1 with the founder | <https://buy.stripe.com/aFa7sNcgAdQS0ZT1Uc8k91t> |

> Refundable. UK Stripe — VAT-clean. Builds on the 81-MCP MEOK fleet.
> Verify any signed report at <https://meok.ai/verify>.

<!-- BUY-LADDER:END -->


## Configuration

Add to your `claude_desktop_config.json` (Claude Desktop) or your MCP client config:

```json
{
  "mcpServers": {
    "agent-commerce-protocol-mcp": {
      "command": "uvx",
      "args": ["agent-commerce-protocol-mcp"]
    }
  }
}
```

Or: `pip install agent-commerce-protocol-mcp` then run the `agent-commerce-protocol-mcp` command (stdio transport).

## Examples

Once configured, ask your assistant, for example:
- "Use `discover_acp_merchants` to …"
- "Use `prepare_payment_intent` to …"
- "Use `sign_payment_intent` to …"

## See also

MEOK compliance MCP fleet:
[`agent-cost-allocator-mcp`](https://github.com/CSOAI-ORG/agent-cost-allocator-mcp), [`agent-identity-trust-mcp`](https://github.com/CSOAI-ORG/agent-identity-trust-mcp), [`agent-orchestrator-mcp`](https://github.com/CSOAI-ORG/agent-orchestrator-mcp), [`agent-replay-debugger-mcp`](https://github.com/CSOAI-ORG/agent-replay-debugger-mcp), [`agent-x402-paywall-mcp`](https://github.com/CSOAI-ORG/agent-x402-paywall-mcp)
