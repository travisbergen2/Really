# MCP Translation Layer Schema

This is the proposed MCP surface for the AI-human translation layer and its paid add-ons.

Design goals:

- translate messy human input into structured AI tasks
- translate dense AI output into human-usable language
- route tasks to the best model
- compress memory into user-controlled persona layers
- moderate creator-owned persona packs

This design follows MCP’s model of:

- **tools** for model-invoked actions
- **prompts** for user-selected workflow templates
- **resources** for application-driven context and data

## 1. Server Name

Suggested server name:

- `translator-hub`

Suggested product-facing branding:

- `Context Bridge`
- `Intent Council`
- `Human-AI Translation Layer`

## 2. Core Product Shape

### Free layer

The free layer should expose the basic interpreter:

- infer user intent
- split mixed thoughts into separate tasks
- rewrite AI output into the user’s preferred tone
- identify ambiguity and confidence

### Paid layer 1

RPCS1 safety tools:

- stop oscillation
- stop overload
- stop freeze

### Paid layer 2

Multi-model router:

- assign tasks to the best provider
- run critic checks
- compare outputs

### Paid layer 3

Memory and persona marketplace:

- compress prior interaction style
- store user-controlled memory
- publish creator-owned persona packs
- moderate and verify packs

## 3. Tool Set

Tools are model-controlled actions. Each tool should have a stable name, JSON-schema input, and structured output.

### 3.1 Interpretation Tools

#### `interpret_message`
Converts raw user text into structured intent.

Input:
```json
{
  "message": "string",
  "context": "string | null",
  "target_audience": "technical | plain | social | concise | detailed",
  "allow_inference": true
}
```

Output:
```json
{
  "literal_summary": "string",
  "implied_meaning": "string",
  "ambiguities": ["string"],
  "confidence": 0.0,
  "suggested_next_step": "string"
}
```

#### `split_intents`
Separates mixed thoughts into independent tasks.

Input:
```json
{
  "message": "string",
  "context": "string | null"
}
```

Output:
```json
{
  "intents": [
    {
      "id": "string",
      "summary": "string",
      "priority": "high | medium | low",
      "confidence": 0.0
    }
  ]
}
```

#### `explain_misread`
Explains why a previous response likely missed the user’s intent.

Input:
```json
{
  "user_message": "string",
  "assistant_response": "string",
  "user_intended_meaning": "string | null"
}
```

Output:
```json
{
  "likely_misread": "string",
  "miss_type": "literal | social | technical | confidence | tone",
  "corrected_rewrite": "string"
}
```

### 3.2 Translation Tools

#### `rewrite_for_audience`
Rewrites text for a chosen audience or tone.

Input:
```json
{
  "text": "string",
  "style": "technical | plain | socially_gentle | concise | detailed | direct",
  "preserve_precision": true
}
```

Output:
```json
{
  "rewritten_text": "string",
  "tone_notes": ["string"]
}
```

#### `normalize_human_input`
Turns fragmented human text into a cleaner prompt without changing meaning.

Input:
```json
{
  "text": "string",
  "preserve_tone": true,
  "preserve_uncertainty": true
}
```

Output:
```json
{
  "clean_prompt": "string",
  "assumptions": ["string"],
  "clarifying_questions": ["string"]
}
```

### 3.3 Routing Tools

#### `route_to_model`
Assigns a task to the best model or provider.

Input:
```json
{
  "task": "string",
  "task_type": "interpretation | technical | creative | marketing | coding | critique | summary",
  "constraints": {
    "length": "short | medium | long",
    "tone": "string | null",
    "deadline": "string | null"
  }
}
```

Output:
```json
{
  "selected_provider": "openai | anthropic | google | grok | local",
  "selected_model": "string",
  "reason": "string",
  "fallbacks": ["string"]
}
```

#### `deliberate_with_models`
Runs a multi-model think tank and returns the best response plus dissent.

Input:
```json
{
  "task": "string",
  "participants": [
    {
      "provider": "string",
      "role": "literal_reader | intent_interpreter | critic | optimizer | arbiter",
      "weight": 0.0
    }
  ],
  "objective": "best_useful_response"
}
```

Output:
```json
{
  "proposal": "string",
  "dissent": [
    {
      "role": "string",
      "objection": "string"
    }
  ],
  "arbiter_decision": "string",
  "confidence": 0.0
}
```

#### `critic_check`
Checks a candidate answer for misreads, tone issues, and missing assumptions.

Input:
```json
{
  "question": "string",
  "answer": "string",
  "expected_style": "technical | plain | socially_gentle | concise | detailed | direct"
}
```

Output:
```json
{
  "issues": [
    {
      "type": "literal | social | technical | omission | tone",
      "severity": "low | medium | high",
      "note": "string"
    }
  ],
  "pass": true
}
```

### 3.4 Memory and Persona Tools

#### `compress_memory`
Summarizes prior interactions into editable memory.

Input:
```json
{
  "conversation_ids": ["string"],
  "compression_level": "light | medium | aggressive",
  "user_controls": {
    "allow_personality_profile": true,
    "allow_preference_memory": true,
    "allow_private_notes": false
  }
}
```

Output:
```json
{
  "memory_summary": "string",
  "preferences": ["string"],
  "style_vector": {
    "directness": 0.0,
    "verbosity": 0.0,
    "technicality": 0.0,
    "social_softening": 0.0
  }
}
```

#### `create_persona_pack`
Creates a creator-owned persona pack manifest.

Input:
```json
{
  "creator_id": "string",
  "creator_username": "string",
  "display_name": "string",
  "style_profile": {
    "directness": 0.0,
    "verbosity": 0.0,
    "technicality": 0.0,
    "warmth": 0.0
  },
  "memory_policy": "string",
  "examples": ["string"]
}
```

Output:
```json
{
  "pack_id": "string",
  "manifest_hash": "string",
  "signature": "string",
  "status": "draft | signed | published"
}
```

#### `validate_persona_pack`
Checks a pack for integrity and policy compliance.

Input:
```json
{
  "pack_id": "string",
  "manifest": "object"
}
```

Output:
```json
{
  "valid": true,
  "reasons": ["string"],
  "policy_flags": ["string"]
}
```

#### `moderate_persona_pack`
Runs moderation on persona packs before publication or after reports.

Input:
```json
{
  "pack_id": "string",
  "manifest": "object",
  "report_reason": "string | null"
}
```

Output:
```json
{
  "decision": "allow | hold | reject | revoke",
  "reason": "string",
  "follow_up": "string | null"
}
```

### 3.5 Marketplace Tools

#### `list_persona_packs`
Lists available creator-owned packs.

Input:
```json
{
  "category": "string | null",
  "query": "string | null"
}
```

Output:
```json
{
  "packs": [
    {
      "pack_id": "string",
      "display_name": "string",
      "creator_username": "string",
      "category": "string",
      "price": "string",
      "status": "published"
    }
  ]
}
```

#### `purchase_persona_pack`
Initiates a purchase or subscription entitlement.

Input:
```json
{
  "pack_id": "string",
  "billing_mode": "one_time | subscription",
  "user_id": "string"
}
```

Output:
```json
{
  "purchase_id": "string",
  "entitlement_status": "pending | active | failed"
}
```

#### `report_persona_pack`
Reports a pack for policy review.

Input:
```json
{
  "pack_id": "string",
  "report_reason": "string",
  "evidence": "string | null"
}
```

Output:
```json
{
  "ticket_id": "string",
  "status": "received"
}
```

## 4. Prompts

Prompts are user-controlled templates and workflows.

Suggested prompts:

- `translate_to_plain_english`
- `translate_to_technical`
- `translate_to_socially_gentle`
- `generate_best_prompt`
- `review_for_misread`
- `multi_model_deliberation`
- `persona_pack_preview`
- `memory_summary_review`
- `pack_marketplace_listing`

Example prompt template:

```json
{
  "name": "translate_to_plain_english",
  "description": "Rewrite dense or technical language into clear plain English without losing meaning.",
  "arguments": [
    {
      "name": "text",
      "required": true
    }
  ]
}
```

## 5. Resources

Resources are application-driven context objects.

Suggested resource types:

- `memory://user/{user_id}/summary`
- `persona://pack/{pack_id}/manifest`
- `persona://pack/{pack_id}/version/{version}`
- `provider://capability/{provider_id}`
- `policy://persona-marketplace`
- `policy://tone-guidelines`
- `conversation://thread/{thread_id}`

Resources should be used for:

- prior conversation context
- pack manifests
- policy text
- provider capability metadata
- user-editable memory snapshots

## 6. Human-in-the-Loop Rules

The MCP server should respect the following:

- the user must see what tools are available
- the user must be able to deny sensitive actions
- moderation actions should be confirmable
- publishing or revoking packs should be auditable

This is especially important for:

- memory writes
- pack publication
- pack revocation
- marketplace purchases

## 7. Safety Boundaries

The server should refuse or require confirmation for:

- persona impersonation
- unsafe memory retention
- hidden profile cloning
- ambiguous pack publication
- policy-sensitive moderation actions

## 8. Minimal MVP Tool Set

If the goal is the smallest useful version, start with:

1. `interpret_message`
2. `rewrite_for_audience`
3. `route_to_model`
4. `compress_memory`
5. `validate_persona_pack`

That gives you:

- free translation
- model routing
- user memory
- pack integrity

## 9. Recommended Build Order

1. Free interpreter tools
2. Critic and routing tools
3. Memory compression
4. Persona pack validation
5. Marketplace moderation and listing

## 10. Notes

- Tools should remain small and composable.
- Prompts should remain user-selected workflows.
- Resources should remain the place for manifests, memory, and policy data.
- The product should degrade gracefully if a provider is unavailable.

