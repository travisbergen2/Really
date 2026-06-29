# RPCS-1 Translation Layer Product Spec

## Product Definition

RPCS-1 is a mutual translation layer between human intent and machine interpretation.

It sits between a user and an AI system and reduces misunderstanding by translating:

- compressed or fragmented human thoughts into clean prompts
- dense or literal AI output into the user’s preferred cognitive style
- socially loaded phrasing into safer, clearer wording
- ambiguous language into explicit intent plus uncertainty markers

The product is not primarily a chatbot, a router, or a marketplace. It is the bridge that makes those later modules usable.

## Core Problem

Humans communicate through:

- implication
- tone
- assumed context
- status cues
- shorthand

AI systems often respond through:

- literal parsing
- over-formal summaries
- probability-weighted interpretation
- safety framing that can feel sterile

That mismatch is especially costly for users who think precisely, type quickly, or communicate in chunks.

## MVP

The first version should do four things very well:

1. **Intent extraction**
   - Identify what the user is actually trying to say or accomplish.

2. **Ambiguity detection**
   - Flag words or phrases that could be misread by humans or AI.

3. **Audience translation**
   - Rewrite the message for a target receiver or tone.

4. **Response normalization**
   - Translate AI output back into the user’s preferred style without losing meaning.

## User Flow

1. User enters messy or compressed language.
2. RPCS-1 shows the inferred intent and likely misreads.
3. User chooses or confirms the target audience.
4. RPCS-1 rewrites the prompt or response.
5. User sends the cleaned version to the AI or to another human.

## Primary Modes

- **AI Prompt Translator**
  - Turns human thought into AI-readable instructions.

- **Human Tone Translator**
  - Turns technical or literal wording into socially safer language.

- **Neurodivergent Bridge**
  - Shows what the speaker probably meant versus what the receiver may hear.

- **Conflict Defuser**
  - Preserves meaning while removing accidental threat, bluntness, or condescension.

## Non-Goals for MVP

Do not start with:

- marketplace features
- personality packs
- multi-model orchestration
- complex memory systems
- model-specific optimization

Those are valuable later, but they are not required to validate the bridge itself.

## Success Criteria

RPCS-1 is useful if it consistently:

- reduces misreads
- preserves uncertainty instead of inflating confidence
- makes technical language understandable without flattening it
- makes social language safer without losing the underlying intent
- helps users move from rough thought to usable instruction faster

## Positioning

Recommended tagline:

> Say what you mean. Hear what they meant.

Alternative framing:

> A translation layer for minds, not languages.

## Roadmap

1. Free translation layer
2. Better audience-aware rewriting
3. Optional routing to specialist models
4. Persistent memory
5. Creator-owned persona packs
6. Marketplace and moderation

The first release should prove the bridge. Everything else is an expansion of that trust.
