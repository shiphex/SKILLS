# Genshin pretraining source policy

## Folder policy

### Preferred folders

Process narrative and descriptive fields from:

`characters`, `archon-quests`, `character-quests`, `event-quests`, `books`, `chronicles`, `artifacts`, `weapons`, `wildlife`, `foods`, and `items`.

### Selective folders

Process `monsters`, `materials`, `quest-items`, `secret-items`, and `namecards` only when a description contains meaningful world-internal prose. Reject records that contain only a name, type, source, use, drop, reward, or other catalog metadata.

### Excluded folders

Always exclude `archon-quest-index` and `character-quest-index`. Exclude unknown folders by default, but list them in the manifest so the policy can be reviewed later.

## Keep

Keep content that answers one of these questions from inside the setting:

- Who is this person, creature, group, or place?
- What happened, what is remembered, or what is believed?
- What does this book, weapon, artifact, food, or object mean in the world?
- What does an NPC or character say, and what does that reveal about them?
- What customs, relationships, conflicts, histories, or local details are described?

Typical acceptable field meanings include `介绍`, `描述`, `故事`, `角色故事`, `传说`, `背景`, `历史`, `正文`, `卷`, `章节`, `角色语音`, `剧情对话`, `旁白`, `相关角色`, `所属`, `种族`, and `任务描述` when the text is narrative rather than an instruction.

`相关角色`, `出场人物`, and similar lists may be used as context for an adjacent narrative, but must not be emitted as a bare list.

## Reject or strip

Reject a field or paragraph when it is primarily:

- player mechanics: attack/defense/health attributes, damage, multipliers, critical stats, cooldowns, energy, level scaling, talents, constellations, builds, or performance/strength comparisons;
- progression or catalog metadata: acquisition, exchange, drops, rewards, costs, materials, enhancement, refinement, ascension, version, duration, event period, or rarity;
- task/UI instructions: objectives, route steps, prerequisites, follow-up tasks, `前往`, `调查`, `击败`, `回到`, `寻找`, or `与……对话` when presented as a checklist or command;
- database residue: field labels, JSON syntax, HTML tags, templates, comments, empty values, repeated separators, or table rows;
- meta language: `玩家`, `角色等级`, `游戏中`, `根据资料`, `攻略`, `推荐`, `配队`, or explanations of how to use the game.

Do not reject an ordinary world sentence only because it contains a word such as “攻击”, “武器”, or “能力”. Reject high-confidence mechanics expressions and UI-shaped fragments. For example, a story saying “魔物攻击了村庄” is acceptable; “攻击力提升 20%” is not.

## Source-grounded rewriting

Use the smallest edit that makes a unit coherent. Preserve named entities and quoted speech. Do not resolve competing accounts, fill missing chronology, infer hidden identity, or explain an ability beyond the source. Keep in-world uncertainty such as “据说”, “传闻”, and “有人认为”.

For dialogue, preserve the speaker when known and keep adjacent turns together. Remove only task commands, menus, or mechanical annotations; do not turn the remaining dialogue into `messages`.

## Output metadata

The main JSONL is intentionally minimal:

```json
{"text":"独立、连贯、事实受源资料支持的世界观文本。"}
```

The manifest should include `format: "jsonl"`, `column: "text"`, `rule_version`, relative `source_root`, output filename, accepted/rejected totals, per-folder counts, unknown folders, unreadable files, and validator status. Each rejected record should include `source`, `reason_codes`, and a short `preview`; never use rejected content as training data.

