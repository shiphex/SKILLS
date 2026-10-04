#!/usr/bin/env python3
"""Validate the minimal JSONL contract used by generate-genshin-pretrain."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


DEFAULT_MIN_CHARS = 100
DEFAULT_MAX_CHARS = 1800

HTML_RE = re.compile(r"<\/?[A-Za-z][^>]*>")
JSON_RE = re.compile(r'^[\s\[\]{},"]+$')
FIELD_DUMP_RE = re.compile(r"(?:^|[\n])\s*[\"']?[A-Za-z_\u4e00-\u9fff][^\n]{0,24}[\"']?\s*[:：]\s*[^\n]+")
TASK_LINE_RE = re.compile(r"^\s*(?:前往|调查|击败|回到|寻找|与.{1,20}对话|保护|收集|进入|返回).{0,80}$")

# Keep this list conservative. World prose may mention fighting, weapons, or attacks.
HIGH_CONFIDENCE_PATTERNS = (
    ("player_meta", re.compile(r"玩家|角色等级|游戏中可以|根据资料|数据集|训练集")),
    ("progression", re.compile(r"获取方式|兑换|掉落|突破材料|精炼材料|强化材料|活动期间|所属版本|前置任务|后续任务")),
    ("build_meta", re.compile(r"配队|攻略|推荐配置|强度排行|性能排行|实战表现")),
    ("combat_stat", re.compile(r"攻击力|防御力|生命值|暴击率|暴击伤害|元素充能效率|伤害加成")),
    ("formula", re.compile(r"倍率|冷却时间|冷却|能量需求|消耗")),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", type=Path, help="JSONL dataset to validate")
    parser.add_argument("--min-chars", type=int, default=DEFAULT_MIN_CHARS)
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    parser.add_argument("--report-json", type=Path, help="Optional machine-readable report")
    return parser.parse_args()


def normalize_for_hash(text: str) -> str:
    return re.sub(r"[\s\u3000，。！？、；：‘’“”《》〈〉（）()「」『』…—\-_,.!?]", "", text)


def classify(text: str, min_chars: int, max_chars: int) -> list[tuple[str, str]]:
    issues: list[tuple[str, str]] = []
    stripped = text.strip()
    if not stripped:
        issues.append(("empty", "text is empty"))
        return issues
    if len(stripped) < min_chars:
        issues.append(("too_short", f"{len(stripped)} characters < {min_chars}"))
    if len(stripped) > max_chars:
        issues.append(("too_long", f"{len(stripped)} characters > {max_chars}"))
    if HTML_RE.search(stripped):
        issues.append(("html", "HTML markup remains"))
    if JSON_RE.fullmatch(stripped):
        issues.append(("database_fragment", "text is only punctuation or JSON syntax"))
    if stripped.startswith("#") or "```" in stripped:
        issues.append(("markdown", "Markdown residue remains"))
    if any(TASK_LINE_RE.fullmatch(line) for line in stripped.splitlines() if line.strip()):
        issues.append(("task_instruction", "checklist-like task instruction remains"))
    if FIELD_DUMP_RE.search(stripped) and ("{" in stripped or '"' in stripped):
        issues.append(("field_dump", "JSON/field-dump residue remains"))
    for code, pattern in HIGH_CONFIDENCE_PATTERNS:
        if pattern.search(stripped):
            issues.append((code, f"high-confidence prohibited phrase: {pattern.pattern}"))
    return issues


def validate(path: Path, min_chars: int, max_chars: int) -> dict[str, object]:
    errors: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []
    hashes: dict[str, int] = {}
    records = 0

    try:
        # PowerShell's UTF-8 writer commonly emits a BOM on Windows.
        handle = path.open("r", encoding="utf-8-sig")
    except OSError as exc:
        return {"path": str(path), "records": 0, "errors": [{"line": 0, "code": "read_error", "message": str(exc)}], "warnings": [], "duplicates": 0}

    with handle:
        for line_no, raw_line in enumerate(handle, 1):
            if not raw_line.strip():
                warnings.append({"line": line_no, "code": "blank_line", "message": "blank lines are ignored"})
                continue
            records += 1
            try:
                item = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                errors.append({"line": line_no, "code": "invalid_json", "message": str(exc)})
                continue
            if not isinstance(item, dict):
                errors.append({"line": line_no, "code": "not_object", "message": "record must be a JSON object"})
                continue
            if set(item) != {"text"}:
                errors.append({"line": line_no, "code": "wrong_keys", "message": f"expected only ['text'], got {sorted(item)}"})
                continue
            if not isinstance(item["text"], str):
                errors.append({"line": line_no, "code": "text_not_string", "message": "text must be a string"})
                continue
            text = item["text"].strip()
            for code, message in classify(text, min_chars, max_chars):
                target = warnings if code == "too_long" else errors
                target.append({"line": line_no, "code": code, "message": message})
            normalized = normalize_for_hash(text)
            if normalized:
                digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
                if digest in hashes:
                    errors.append({"line": line_no, "code": "duplicate", "message": f"duplicate of line {hashes[digest]}"})
                else:
                    hashes[digest] = line_no

    return {"path": str(path), "records": records, "errors": errors, "warnings": warnings, "duplicates": sum(1 for item in errors if item["code"] == "duplicate")}


def main() -> int:
    args = parse_args()
    if args.min_chars < 0 or args.max_chars < args.min_chars:
        print("invalid length bounds", file=sys.stderr)
        return 2
    report = validate(args.dataset, args.min_chars, args.max_chars)
    if args.report_json:
        args.report_json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"validated {report['path']}: {report['records']} records, {len(report['errors'])} errors, {len(report['warnings'])} warnings")
    for item in report["errors"][:20]:
        print(f"ERROR line {item['line']}: [{item['code']}] {item['message']}", file=sys.stderr)
    for item in report["warnings"][:20]:
        print(f"WARN line {item['line']}: [{item['code']}] {item['message']}", file=sys.stderr)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
