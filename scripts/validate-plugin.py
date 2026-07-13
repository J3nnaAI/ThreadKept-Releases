#!/usr/bin/env python3
"""Validate the shipped plugin/extension manifests against each tool's contract.

This is machinery, not memory: it caught (and now prevents the return of) the defect
where the Claude Code plugin was NOT installable because .claude-plugin/marketplace.json
was missing — the documented /plugin install simply could not work. It runs in CI on
every push (see .github/workflows/validate.yml).

It checks what is checkable WITHOUT a real tool install (JSON validity, required
manifests present, referenced files exist, hook commands portable, event names match
each tool's contract). What it CANNOT check — that the arrival packet actually renders
inside a live Claude Code / Codex / Gemini session — is the operator verification
punch-list, not something this script pretends to cover.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []


def err(msg):
    errors.append(msg)


def load(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        err(f"MISSING file: {rel}")
        return None
    try:
        with open(p) as f:
            return json.load(f)
    except Exception as e:
        err(f"INVALID JSON in {rel}: {e}")
        return None


def exists(rel):
    return os.path.exists(os.path.join(ROOT, rel))


# --- Claude Code: a repo-root plugin is installable ONLY via a marketplace manifest ---
mkt = load(".claude-plugin/marketplace.json")
if mkt is not None:
    if not mkt.get("name"):
        err("marketplace.json: missing 'name'")
    if not (mkt.get("owner") or {}).get("name"):
        err("marketplace.json: missing owner.name")
    plugins = mkt.get("plugins") or []
    if not plugins:
        err("marketplace.json: 'plugins' is empty — nothing is installable")
    for p in plugins:
        if not p.get("name") or not p.get("source"):
            err(f"marketplace.json: a plugin entry needs name+source: {p}")
        src = p.get("source", "")
        # source './' means the plugin manifest is at the repo root
        if src in ("./", ".") and not exists(".claude-plugin/plugin.json"):
            err("marketplace.json points a plugin at './' but .claude-plugin/plugin.json is missing")

load(".claude-plugin/plugin.json")

# --- Codex: manifest must point at a hooks file that EXISTS ---
codex = load(".codex-plugin/plugin.json")
if codex is not None:
    h = codex.get("hooks")
    if isinstance(h, str) and not exists(h.lstrip("./")):
        err(f".codex-plugin: hooks -> {h} does not exist")
    # THE LAW (enumerated across ecosystems): a repo-root plugin is installable ONLY via
    # its ecosystem's MARKETPLACE manifest. Claude Code -> .claude-plugin/marketplace.json;
    # Codex -> .agents/plugins/marketplace.json. Iteration 1 fixed Claude Code; the class
    # was 'every shipping ecosystem's marketplace manifest', and Codex was the next member.
    cmkt = load(".agents/plugins/marketplace.json")  # load() errs "MISSING file" if absent
    if cmkt is not None:
        if not cmkt.get("name"):
            err(".agents/plugins/marketplace.json: missing 'name'")
        cplugins = cmkt.get("plugins") or []
        if not cplugins:
            err(".agents/plugins/marketplace.json: 'plugins' is empty — the Codex plugin is not installable")
        for p in cplugins:
            src = p.get("source") if isinstance(p.get("source"), dict) else {}
            path = src.get("path")
            if not p.get("name") or not path:
                err(f".agents/plugins/marketplace.json: plugin entry needs name + source.path: {p}")
            elif path in ("./", ".") and not exists(".codex-plugin/plugin.json"):
                err(".agents marketplace points a plugin at './' but .codex-plugin/plugin.json is missing")

# --- Gemini: extension manifest + its context file ---
gem = load("gemini-extension.json")
if gem is not None:
    cf = gem.get("contextFileName", "GEMINI.md")
    if not exists(cf):
        err(f"gemini-extension.json: contextFileName '{cf}' does not exist")
    if "mcpServers" not in gem:
        err("gemini-extension.json: no mcpServers (the tools would be absent)")
    # GEMINI.md is Gemini's resident protocol — the THIRD instruction door alongside the
    # hydrate arrival packet (hooked tools) and AGENTS.md (universal). All three must carry
    # the same disciplines or a Gemini agent gets a weaker protocol than a Claude Code one.
    # (agentsMD is guarded by TestAgentsMDCarriesTheResidentDisciplines; the packet by
    # policy_test.go; this is GEMINI.md's guard, so the three cannot drift apart.)
    cf = gem.get("contextFileName", "GEMINI.md")
    if exists(cf):
        with open(os.path.join(ROOT, cf)) as f:
            g = f.read().lower()
        for disc in ("hydrate", "recall", "grounds", "supersede"):
            if disc not in g:
                err(f"{cf} is missing the resident discipline '{disc}' (the instruction doors must not drift)")

# --- every hooks file: valid JSON, portable commands, right events for its tool ---
CLAUDE_EVENTS = {"SessionStart", "PreCompact", "UserPromptSubmit", "PostToolUse", "PreToolUse", "Stop"}
for rel, allowed in [("hooks/hooks.json", CLAUDE_EVENTS), ("hooks/codex-hooks.json", CLAUDE_EVENTS)]:
    h = load(rel)
    if h is None:
        continue
    events = h.get("hooks", h)
    for ev, arr in events.items():
        if ev not in allowed:
            err(f"{rel}: event '{ev}' is not a valid event for this tool")
        for matcher in arr:
            for hook in matcher.get("hooks", []):
                cmd = hook.get("command", "")
                if "CLAUDE_PLUGIN_ROOT" in cmd or cmd.startswith("/") or "/home/" in cmd:
                    err(f"{rel}: non-portable hook command: {cmd!r}")
                if not cmd.startswith("threadkept "):
                    err(f"{rel}: hook command should invoke 'threadkept <verb>': {cmd!r}")

# --- skills: /threadkept:setup and :status must exist, and setup must NOT instruct
# 'threadkept setup' — that writes a SECOND hookset beside the plugin's own, and they
# double-fire (a real, load-bearing trap). Guard the double-wire warning stays present.
for sk in ("skills/setup/SKILL.md", "skills/status/SKILL.md"):
    if not exists(sk):
        err(f"missing skill {sk} — the plugin's /threadkept command would not exist")
_setup = os.path.join(ROOT, "skills/setup/SKILL.md")
if os.path.exists(_setup):
    txt = open(_setup).read().lower()
    if "do not run" not in txt or "threadkept setup" not in txt:
        err("skills/setup/SKILL.md lost the double-wire warning ('Do NOT run threadkept setup' beside the plugin's hooks)")

if errors:
    print("PLUGIN VALIDATION FAILED:")
    for e in errors:
        print("  - " + e)
    sys.exit(1)
print("plugin validation OK — all manifests valid, referenced files present, commands portable, events per-tool")
