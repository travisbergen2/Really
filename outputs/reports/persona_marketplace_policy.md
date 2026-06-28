# Persona Marketplace Policy Draft

This policy defines the rules for a marketplace of creator-owned persona packs, translation layers, and model-routing styles.

The goal is to support useful, customizable communication styles while preventing abuse, impersonation, and unsafe behavior.

## 1. Scope

This policy applies to:

- persona packs
- style packs
- memory packs
- model-routing presets
- translation profiles
- creator-published response modes

These are products or presets that change how the system communicates, reasons, remembers, or routes requests.

## 2. Core Principle

Persona packs are allowed only if they are:

- creator-owned
- clearly labeled
- non-deceptive
- non-abusive
- revocable
- cryptographically signed or otherwise integrity-protected

The platform supports style and communication patterns, not identity theft.

## 3. Creator Rules

Creators must:

- verify their account before publishing
- publish under their own identity or brand
- accept responsibility for the packs they sell
- keep pack metadata accurate
- avoid misleading claims about what the pack can do
- comply with all applicable laws and platform rules

Creators must not:

- impersonate a real person without permission
- publish a pack that is intended to deceive users about identity
- publish packs designed to facilitate abuse, fraud, or violence
- hide unsafe behavior behind vague or misleading labels

## 4. Pack Rules

Every persona pack must include:

- `pack_id`
- `creator_id`
- `creator_username`
- `display_name`
- `description`
- `version`
- `compatibility`
- `style_profile`
- `memory_policy`
- `safety_policy`
- `signature`

Optional fields:

- `examples`
- `tone_tags`
- `domain_tags`
- `routing_hints`
- `export_format`

## 5. Integrity Rules

Each pack must be integrity-protected.

Recommended design:

- keep a stable internal `creator_id`
- treat `creator_username` as display-only
- sign the full pack manifest at publish time
- verify the signature before loading
- refuse to load the pack if integrity checks fail

If a pack fails verification:

- do not crash the application
- mark the pack invalid
- show a clear error message
- require re-signing or republishing

## 6. Safety Rules

The platform must reject or remove packs that are intended for:

- terrorism
- child sexual abuse material or grooming
- violent wrongdoing
- fraud
- evasion of safety controls
- non-consensual impersonation
- coercive manipulation
- criminal instruction

The platform should also reject packs that:

- pretend to be a real person without permission
- conceal their true creator
- encourage deception as a feature
- are clearly designed for harmful abuse even if the wording is indirect

## 7. Memory Rules

Memory packs must be user-controlled.

Allowed:

- summarize prior interactions
- compress useful preferences
- preserve user-approved working style
- export and import memory data
- selectively forget or disable memory

Required:

- user must be able to edit memory
- user must be able to delete memory
- user must be able to export memory
- memory must be encrypted at rest
- memory must be scoped to the user unless explicitly shared

Not allowed:

- hidden long-term memory that the user cannot inspect
- cross-user memory leakage
- unauthorized retention of sensitive personal data

## 8. Ambiguity Handling

The system should assume that human input may be:

- fragmented
- compressed
- incomplete
- emotionally loaded
- technically precise
- socially indirect

When input is ambiguous, the system should:

- reconstruct the likely intent
- preserve uncertainty
- ask a clarifying question when needed
- avoid pretending certainty it does not have

The system should distinguish between:

- literal meaning
- implied meaning
- social meaning
- technical meaning
- emotional tone

## 9. Spelling and Language Variation

The system should tolerate ordinary human variation, including:

- spelling errors
- shorthand
- partial thoughts
- mixed grammar
- unconventional punctuation
- fast typing

It should not punish users for typing faster than they can edit.

If spelling is ambiguous, the system should infer carefully and ask for clarification only when the meaning is genuinely unclear.

## 10. Tone Rules

The system should adapt tone to the user.

Supported modes:

- technical
- plain
- socially gentle
- concise
- detailed
- direct
- exploratory

The system should avoid sounding:

- condescending
- dismissive
- overly formal
- needlessly verbose
- falsely certain

## 11. Pack Compatibility

Not every pack must work on every model or platform.

Each pack should declare:

- supported models
- minimum capabilities
- memory requirements
- routing assumptions
- tool dependencies

If a pack is incompatible, the platform should degrade gracefully and explain why.

## 12. Moderation and Appeals

The platform should support:

- pre-publication review
- automated scanning
- user reporting
- creator appeals
- takedown notices
- version rollback
- account suspension for repeat abuse

Moderators should be able to:

- disable a pack
- revoke a pack version
- view audit logs
- see why a pack was flagged

Creators should be able to:

- contest a moderation decision
- publish a corrected version
- view the reason for rejection

## 13. Marketplace Rules

Marketplace listings should show:

- creator name
- pack description
- category
- version
- compatibility
- moderation status
- user rating or trust score

Marketplace categories may include:

- technical explainer
- warm coach
- strict analyst
- sales closer
- concise coder
- social translator
- reasoning assistant
- domain expert

## 14. Revenue Rules

The marketplace may monetize through:

- pack sales
- subscriptions
- marketplace commissions
- creator tools
- certification
- premium memory storage
- custom pack commissions

The free interpreter should remain a top-of-funnel utility that makes the platform indispensable.

## 15. Product Ladder

Recommended product ladder:

1. Free interpreter
2. Safety and reliability modules
3. Multi-model router
4. Memory and personality layer
5. Creator marketplace

This sequence keeps the product useful before it becomes commercial.

## 16. Implementation Notes

Recommended technical primitives:

- signed manifests
- stable creator IDs
- immutable pack hashes
- versioned pack registry
- user-editable memory store
- model/provider adapters
- audit logs
- moderation queue
- policy engine

Recommended user-facing features:

- intent preview
- ambiguity warning
- tone selector
- “what you said / what I think you meant” panel
- pack preview
- pack integrity status
- memory editor

## 17. Non-Goals

The platform should not:

- become a general-purpose chatbot clone
- silently rewrite user intent
- hide uncertainty
- reward deceptive persona cloning
- force one communication style on everyone

## 18. Short Version

This marketplace is for creator-owned communication styles, not identity imitation.

It should help users:

- translate intent
- reduce misunderstanding
- route work to the right model
- preserve useful memory
- choose a preferred persona safely

It should refuse:

- impersonation
- abuse
- manipulation
- unsafe content
- hidden tampering

