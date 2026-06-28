# MCP Translation Layer Build Plan

This plan turns the translation-layer concept into an executable product.

The objective is to ship the free interpreter first, then layer paid routing, memory, and persona-marketplace capabilities on top.

## 1. Product Summary

The product is a lightweight MCP server plus optional host UI that sits between the user and one or more AI providers.

Core functions:

- translate messy human input into structured intent
- rewrite AI output into the user’s expected register
- route tasks to the best model
- compress memory into editable user-owned profiles
- validate and moderate creator-owned persona packs

## 2. MVP Goal

The first shippable version should do three things well:

1. Clean up fragmented user input without changing meaning.
2. Rewrite responses for a chosen audience or tone.
3. Route a request to the best model/provider and return a structured result.

If those three work, the rest becomes an expansion problem rather than a feasibility problem.

## 3. Repository Structure

Suggested layout:

```text
translator-hub/
├── README.md
├── pyproject.toml
├── src/
│   └── translator_hub/
│       ├── __init__.py
│       ├── server.py
│       ├── manifest.py
│       ├── schema/
│       │   ├── tools.py
│       │   ├── prompts.py
│       │   └── resources.py
│       ├── tools/
│       │   ├── interpret.py
│       │   ├── rewrite.py
│       │   ├── route.py
│       │   ├── deliberate.py
│       │   ├── memory.py
│       │   ├── persona.py
│       │   └── moderation.py
│       ├── providers/
│       │   ├── openai.py
│       │   ├── anthropic.py
│       │   ├── google.py
│       │   ├── grok.py
│       │   └── local.py
│       ├── policy/
│       │   ├── marketplace.py
│       │   ├── memory.py
│       │   └── safety.py
│       └── storage/
│           ├── memory_store.py
│           └── pack_registry.py
├── ui/
│   └── web/
│       ├── app/
│       └── components/
└── docs/
    ├── architecture.md
    ├── marketplace_policy.md
    └── tool_reference.md
```

## 4. MCP Manifest Shape

The MCP server should declare:

- server name: `translator-hub`
- version: semantic versioning
- tools: the action surface
- prompts: the user-facing workflows
- resources: memory, policy, manifests, and provider capability metadata

### Minimal manifest contents

- `interpret_message`
- `split_intents`
- `rewrite_for_audience`
- `normalize_human_input`
- `route_to_model`
- `deliberate_with_models`
- `critic_check`
- `compress_memory`
- `create_persona_pack`
- `validate_persona_pack`
- `moderate_persona_pack`
- `list_persona_packs`
- `purchase_persona_pack`
- `report_persona_pack`

## 5. Implementation Order

### Phase 1: Free Interpreter

Build first:

- `interpret_message`
- `split_intents`
- `rewrite_for_audience`
- `normalize_human_input`

Deliverable:

- a working MCP server that can turn messy language into clean intent and back again

### Phase 2: Routing Core

Build next:

- `route_to_model`
- `deliberate_with_models`
- `critic_check`

Deliverable:

- provider selection based on task type and constraints
- multi-model deliberation with an arbiter output

### Phase 3: Memory Layer

Build after routing:

- `compress_memory`
- editable memory resources
- user-controlled memory export/delete flows

Deliverable:

- a persistent but user-owned memory summary and style vector

### Phase 4: Persona Pack System

Build after memory:

- `create_persona_pack`
- `validate_persona_pack`
- signed manifests
- pack registry

Deliverable:

- creator-owned persona packs that can be loaded safely and revoked if tampered with

### Phase 5: Marketplace and Moderation

Build last for the MVP line:

- `list_persona_packs`
- `purchase_persona_pack`
- `report_persona_pack`
- moderation queue
- takedown/revocation flow

Deliverable:

- a safe marketplace for creator-owned communication styles

## 6. First UI Flow

The first UI should be simple and show the translation value immediately.

### Screen 1: Compose

User enters messy or compressed text.

Display:

- raw input
- inferred intent
- ambiguities
- confidence
- suggested next prompt

### Screen 2: Rewrite

User selects a target tone.

Display:

- technical version
- plain version
- socially gentle version
- direct version

### Screen 3: Route

User sends a task for model selection.

Display:

- selected provider
- selected model
- reason for selection
- fallback model

### Screen 4: Memory / Persona

User views and edits memory summaries and selected persona packs.

Display:

- current style profile
- editable memory notes
- pack integrity status
- active persona pack

## 7. Tool Contracts

Each tool should return structured JSON, not just prose.

Required metadata on every tool result:

- `confidence`
- `reason`
- `assumptions`
- `ambiguities`
- `suggested_next_step`

This keeps the translator honest and makes misreads easy to spot.

## 8. Provider Routing Strategy

Start with a simple routing table:

- technical long-form work -> Claude
- messy interpretation and synthesis -> ChatGPT
- broad factual triage and concise coding -> Gemini
- marketing and public-facing compression -> Grok

Then make routing adjustable by benchmark results instead of freezing it permanently.

## 9. Safety and Policy

The build must enforce:

- creator-owned personas only
- signed manifests
- integrity validation on load
- user-owned memory
- moderation for unsafe packs
- clear refusal behavior for harmful content

The product should fail closed on tampered or unsafe persona packs.

## 10. Acceptance Criteria

### Free interpreter passes when:

- it can reconstruct a fragmented message into a clean prompt
- it can preserve uncertainty
- it can rewrite the same content for different audiences without changing the meaning

### Router passes when:

- it can explain why a provider was chosen
- it can fall back to another model if the first choice fails

### Memory passes when:

- the user can inspect, edit, delete, and export memory

### Persona pack passes when:

- the pack is signed
- tampering is detected
- invalid packs do not load

## 11. Build Dependencies

You will need:

- one MCP server implementation
- one provider abstraction layer
- persistent storage for memory and packs
- a basic web UI or client
- a policy engine
- a small benchmark suite for translation quality

## 12. First Revenue Path

The most practical initial revenue path is:

1. free interpreter
2. paid routing and safety add-ons
3. persona-memory pack subscriptions
4. creator marketplace fees

This keeps the free layer useful while making the premium layers feel natural.

## 13. What Not To Build First

Do not start with:

- full marketplace complexity
- celebrity-style packs
- complex social-network features
- multi-device sync
- enterprise admin tooling

Those can come later after the interpreter proves value.

## 14. Immediate Next Step

Build the free interpreter as an MCP server with:

- `interpret_message`
- `normalize_human_input`
- `rewrite_for_audience`

Then add the routing core once the first layer is stable.

