---
name: generate-genshin-pretrain
description: Generate and validate Chinese Genshin Impact pretraining JSONL from workspace/raw/parsed worldbuilding files. Use when a local LLM must turn parsed character stories, quests, books, chronicles, item lore, or NPC dialogue into coherent in-world text for workspace/output/Pretrain, while excluding player-facing mechanics, progression, acquisition data, and SFT chat formats.
---

# Generate Genshin Pretrain

Generate a small, factual, world-internal corpus for next-token pretraining. This skill teaches setting knowledge, narrative Chinese, character voice, and NPC/world descriptions; it does not create SFT conversations or system prompts.

## Read before processing

Read [references/source-policy.md](references/source-policy.md) before selecting fields or folders. Run `scripts/validate_pretrain_jsonl.py` after producing each output batch and before publishing the final dataset.

## Fixed paths and output contract

- Input root: `workspace/raw/parsed/`.
- Output root: `workspace/output/Pretrain/`.
- Main dataset: a JSONL file whose every line is exactly `{"text":"..."}`.
- Sidecars: a manifest JSON and a rejected JSONL file with source paths and rejection reasons.
- Never write `messages`, `prompt`, `completion`, `instruction`, role labels, or system prompts to the pretraining dataset.

If `Pretrain/` or the requested output filename already exists, never delete or overwrite it. Use a timestamped filename such as `genshin_pretrain_20260804_153000.jsonl` and matching sidecar names. Write to a temporary file, validate it, then move it into `Pretrain/`.

## Workflow

1. Enumerate JSON files under the input root. Record all discovered folders, including unknown folders, in the manifest; process only the preferred and selective folders in the source policy.
2. Read one file at a time and keep only the fields and paragraphs that describe the world, a person, a story, a book, a place, a creature, an object, or an in-world utterance. Do not load the entire corpus into context.
3. Recursively unwrap nested objects and arrays. Preserve the field path while classifying it, but never emit that path as training text.
4. Remove UI labels, task instructions, acquisition/progression information, combat formulas, numerical attributes, HTML, empty objects, and table-like fragments. When a field mixes lore and mechanics, keep only complete narrative paragraphs.
5. Group related paragraphs by one source entity or one continuous quest/dialogue unit. Do not concatenate unrelated entities merely to meet a length target.
6. Lightly rewrite each accepted unit in fluent Chinese:
   - repair broken joins caused by JSON fields and normalize whitespace;
   - preserve names, relationships, chronology, uncertainty, quotations, and distinctive voice;
   - do not invent facts, motives, events, dialogue, locations, or abilities;
   - do not mention the source, dataset, game UI, player, or the rewriting process.
7. Keep each sample self-contained and normally 100–1800 Chinese characters. Split long material at paragraph or scene boundaries. Merge short adjacent passages only when they belong to the same entity or scene; reject isolated names, labels, and tiny fragments.
8. Keep quest and NPC dialogue as readable transcript prose, for example `克朗谢说：“……”` or `派蒙问道：“……”`; do not convert it into chat-message objects.
9. Emit one JSON object per line with UTF-8 encoding. Validate incrementally. Send invalid or uncertain units to `rejected.jsonl` instead of guessing.
10. Finish `manifest.json` with rule version, input root, output filename, counts, folder statistics, and validation status. Report any unknown folders and unreadable files.

## Generation guardrails for a small LLM

Use short batches: inspect one source file, draft only its accepted units, self-check each draft against the source, and write the batch before continuing. Prefer extraction plus light repair over creative expansion. If a fact is ambiguous, retain the ambiguity in the original wording or reject the unit.

Before accepting a sample, ask:

- Is this understandable without a field name or UI context?
- Is every important claim supported by the source unit?
- Does it belong to Teyvat's world, history, people, creatures, objects, or speech?
- Does it avoid player-only knowledge such as stats, builds, rewards, progression, and task instructions?
- Does it read as natural Chinese rather than a database dump?
- Is it useful for learning setting knowledge or a character/NPC's voice?

Do not turn a story into a tutorial, explain combat strength, rank characters or weapons, describe optimal use, or add an answer to a player question. Those behaviors belong to later SFT/DPO datasets.

## Validation

Run:

```text
python skills/generate-genshin-pretrain/scripts/validate_pretrain_jsonl.py <dataset.jsonl>
```

Treat any error as a failed batch. Warnings require review and should be recorded in the manifest. The validator checks exact JSONL shape, length, duplicates, markup, obvious metadata, and high-confidence player-facing mechanics. It is a guardrail, not a substitute for source-grounded review.

