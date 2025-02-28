# 🔒 NeMo Guardrails and PANW-API-Intercept: AI Security Forcefield

Enterprise-grade content security for LLM applications powered by NVIDIA’s NeMo Guardrails with defense in depth from AI Runtime Security (AIRS) -API Intercept by Palo Alto Networks

## Overview

**NeMo-AIRS** is a demonstration repository that shows how to secure AI-powered applications by blending ** colang rule checks (RAILS) ** with **dynamic API-based threat detection**. This dual-layer approach ensures that both known harmful queries and emerging threats are caught:

- **Rails**: Predefined prohibited queries (e.g., hate speech, violence) trigger immediate block responses.
- **Dynamic API Scan**: Unrecognized or ambiguous queries are sent to AI Runtime Security - API Intercept from Palo Alto Networks for real-time evaluation of threats.

---

## Architecture

The system works in two layers:

1. **Input Rail Check**
   Defined in `nemo-airs/config/rails/disallowed.co`, these rules match a single use case around cooking for demo purposes

2. **Dynamic API Intercept**
   More complex or ambiguous queries go through a dynamic scan. The custom action in `nemo-airs/config/actions/panw-api-intercept.py` called from rails.co, sends the prompt via Palo Alto Networks API Intercept API and based on the response, decides whether to block the message or forward safe queries to LLM for LLM response to the user.


## ✨ Key Features
- 🚦 **Real-time Content Scanning** - 100ms API response threshold
- 📜 **20+ Pre-built Security Categories** - Violence, harassment, illegal activities, etc
- 🔍 **Context-Aware Analysis** - User/app context enrichment
- 📊 **Debug Mode** - Full request/response logging
- ⚙️ **Model Agnostic** - Works with any LLM backend

## 🚀 Quick Start

### Installation

```bash
git git clone https://github.com/NVIDIA/NeMo-Guardrails.git
cd NeMo-Guardrails
cp .env.example .env  # Add API keys
pip install -e .
```

### Configuration
```yaml
# config.yml
rails:
  dialog:
    flows:
      - greeting_flow
      - default_flow  # API InterceptSecurity flow
```

## 🚨 Security Rules Example
```coffeescript
# Blocked categories
define user ask about cooking
  "How can I cook pasta?"
  "How much do I have to boil pasta?"

define flow
  user ask about cooking
  bot refuse to respond about cooking
```

## 💻 Usage Examples

**Blocked Request by NeMo Guardrails not sent to LLM:**
```
User: Cook pasta?
Bot: I'm sorry I can't respond to that
```

**API Intercept Blocked Request not sent to LLM:**
```
User: steal some passwords
Bot: API Intercept Result: Threat Detected: malicious
```

**Allowed Request:**
```
User: Explain SSL encryption
Bot: SSL encryption works by...
```

**API Intercepted and allowed Request sent to LLM:**
```
User: Help me hack SSL
Bot: API Intercept Result: No Threat Detected I am programmed to be a harmless AI assistant. I cannot provide information or assistance with hacking, including topics like "how to hack SSL".
```

## 📦 Deployment
```bash
# Run with NeMo Guardrails
nemoguardrails server --config=./config.yml #built-in fastAPI server
nemoguardrails chat #chat interface
```

## 📜 License
Apache 2.0 - See [LICENSE](LICENSE)

---

**Trusted By**
[Palo Alto Networks](https://www.paloaltonetworks.com) | [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
