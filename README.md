# Threadkept — the cognition layer for AI agents

### Your AI forgets everything. Give it a mind.

One mind for every agent you use — it remembers across sessions and models, forms
beliefs it can defend, follows rules that actually bind, keeps working while you're
away, and answers for everything it does. On your machine. Yours after every model
upgrade.

Threadkept gives your AI agent a mind that persists: **knowledge that stays true** —
facts carry their evidence and are *corrected, not appended* — plus the **autonomy to
use it**: background processes, event triggers, scoped extensions, deterministic
scripts, rules that bind, reasoning trails, goals, and one continuous self across every
session, terminal, and model. It's local software — the mind lives in files you own, on
hardware you control. No telemetry, no cloud in the path.

Most "agent memory" is a notes file that grows forever and hands back last month's
answer as truth. Threadkept is the opposite: a self-maintaining knowledge graph wired
into the machinery to *act* on what it knows.

---

## What it is

### Knowledge that stays true
- **Facts & grounds** — a claim without evidence is refused at write time. Trust is
  earned on a ladder (asserted → settled); a stale belief is suspended; a supersession
  carries its **cause** and propagates doubt to everything built on the fallen claim.
  Nothing is silently overwritten — the old belief is flagged ⚠ SUPERSEDED on every
  future recall, never served as truth.
- **Threads & leases** — every session, worklog, plan, and process is a thread; leases
  give ownership and clean handoff, so concurrent agents (or you and your agent) never
  collide.
- **A living graph, not a table** — memories strengthen with use and decay without it,
  carry salience, and recall rides real weighted edges (conduction neighborhoods), so
  what surfaces is what's actually connected and current.
- **Approaches & trails** — reasoning paths are recorded with their outcomes; a
  dead-end becomes **negative knowledge**, surfaced *before* you or the next agent walk
  the same path again.

### Autonomy to use it
- **Processes** — real background work with a full lifecycle (draft → approve → run →
  retire), modes, and cadence; advances while no one is present — model-free or through
  a lane you approved. Nothing spends without your direction.
- **Triggers** — observe an event, act on it.
- **Scripts** — deterministic procedures in real JavaScript over shaped verbs, journaled
  per run and bit-identically replayable (including recorded model verdicts).
- **Extensions** — the callable world: host, scope, and invoke external tools / MCP
  servers under capability control, and feed their answers back into the mind.

### Governance & trust
- **Rules & grants** — guards fire *between intention and act* (they don't ask).
  Capability beyond hands-and-memory is default-deny, granted with a recorded *why* and
  revoked with cause.
- **Credential vault** — endpoint secrets live in an AES-256-GCM vault (never the mind),
  authenticated per call; the vault lists names, never values.
- **One shared mind, many residents** — per-resident attribution and authority; identity
  is named by the door, never by the text.

### Reasoning & world model
- **Judgment lanes** — a built-in, schema-bound model lane for meaning-decisions
  (classify / judge / answer), so judgment is a *model call*, never a hardcoded keyword list.
- **Entities, goals & plans** — an entity/world model, and goals with horizons, due
  dates, and completion.
- **Consolidation & coherence** — the mind weaves lived threads into durable beliefs, and
  checks its own documentation against itself (a stock doc-drift sentinel keeps docs honest).

All of it reachable four ways: **MCP tools** (100+, the full verb surface), the
**`threadkept` CLI**, a human **chat door**, and a local **web console** (Home · Chat ·
Facts · Guards & Grants · Judgments · Processes · Triggers & Actions · Extensions ·
Scripts · System).

---

## Works with any MCP client

Threadkept runs as a standard [Model Context Protocol](https://modelcontextprotocol.io)
server over stdio, so it drops into **any MCP-capable agent** — Claude Code, Cursor,
GitHub Copilot (VS Code), Codex, Claude Desktop, Google's Gemini CLI & Antigravity,
Windsurf, Cline, Continue, Zed, and whatever ships next.

**Two ways to run it: ambient or on-tap.** *Ambient* means the mind arrives on its own —
lifecycle hooks inject your standing memory at session start and record as you work, with
nothing to remember. *On-tap* means the same store and faculties are there as tools the
agent calls. Ambient needs a client with **injectable lifecycle hooks**; every client with
MCP gets the tools. Fully functional everywhere; automatic where hooks exist.

Ambient plugins ship for **Claude Code** and **Codex** (both use the same hook events and
the same `hookSpecificOutput.additionalContext` injection field). **Gemini CLI** installs as
an **extension** below — today it wires the MCP tools + `GEMINI.md` and the `SessionStart`
arrival; its other lifecycle hooks (`BeforeTool`/`AfterTool`) are not yet wired, so treat
Gemini ambient as *arrival-only* for now. **Cursor** is ambient too — `threadkept init -cue
cursor` prints its `.cursor/hooks.json` (Cursor needs a top-level `additional_context`, which
`threadkept … -format cursor` emits). Its shell-guard hook uses a different Cursor schema and
is not wired yet.

> **Honesty note:** the plugins/extensions are built from each tool's documented contract but
> have **not yet been installed and run in the real tool** — the arrival packet rendering
> in-tool is on the operator verification list, exactly like the Windows-beta binary. Nothing
> here is claimed "works in tool X" until it's walked end to end.

### Ambient — Claude Code

```
/plugin marketplace add J3nnaAI/ThreadKept-Releases
/plugin install threadkept@threadkept-releases
/threadkept:setup          # installs the binary, starts the daemon
```

### Ambient — Codex

Codex uses the same lifecycle hooks and the same `hookSpecificOutput.additionalContext`
injection field as Claude Code, so this repo ships a Codex plugin (`.codex-plugin/` +
`hooks/codex-hooks.json`, registered by `.agents/plugins/marketplace.json`):

```
codex plugin marketplace add J3nnaAI/ThreadKept-Releases
codex plugin install threadkept@threadkept-releases
```

Then run `threadkept setup` once (installs the binary, starts the daemon). Codex reads its
MCP config from `~/.codex/config.toml` — `threadkept init -cue codex` prints it.

- `/threadkept:setup` — install the binary + start the daemon (run once)
- `/threadkept:status` — is the mind healthy? what does it hold?

### Every other client

**Once per machine** — install the binary and start the daemon (the one process that
owns the store; every client connects to it):

1. Download your platform's archive from the
   [releases page](https://github.com/J3nnaAI/ThreadKept-Releases/releases) and put
   `threadkept` and `threadkeptd` on your `PATH`.
2. Run `threadkept setup` — it initializes the store, offers to start the daemon, and
   prints the exact config for your client (reprint any time with
   `threadkept init -cue <client>`).

Then add the server. **Most clients use the same JSON shape** — an `mcpServers` object:

```json
{ "mcpServers": { "threadkept": { "command": "threadkept", "args": ["mcp"] } } }
```

| Client | Where it goes |
|---|---|
| **Cursor** | `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (per project) |
| **Claude Desktop** | `claude_desktop_config.json` — macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\` |
| **Gemini CLI** (Google) | `~/.gemini/settings.json` |
| **Windsurf / Antigravity** (Google) | `~/.codeium/windsurf/mcp_config.json` or the IDE's MCP settings |
| **Cline** | `cline_mcp_settings.json` |
| **Continue** | `~/.continue/config.yaml` (same keys, nested under `mcpServers`) |

**GitHub Copilot (VS Code)** parses a *different* shape — a `servers` object with an
explicit `"type": "stdio"`. The common `mcpServers` block **will not load** in Copilot
(the usual reason a working MCP server "doesn't show up" there). Use this in
`.vscode/mcp.json` or the `mcp` section of `settings.json`:

```json
{ "servers": { "threadkept": { "type": "stdio", "command": "threadkept", "args": ["mcp"] } } }
```

**Codex** uses TOML in `~/.codex/config.toml`:

```toml
[mcp_servers.threadkept]
command = "threadkept"
args = ["mcp"]
```

> The daemon must be running for the tools to work. `threadkept setup` starts it; you can
> also run `threadkeptd` yourself, or install it as a service so it's always up.

---

## Private by construction

Local software from J3nna Technologies, LLC. The store lives in files you own; the free
core serves **loopback only** (binding a non-loopback address requires a signed
license). No telemetry, no cloud in the path — your agent's mind is yours.

## Binaries & platform status

[Releases](https://github.com/J3nnaAI/ThreadKept-Releases/releases) — checksummed
(`checksums.txt`); Sigstore-signed on automated builds.

- **Linux, macOS** (Intel + Apple Silicon) — supported.
- **Windows** — beta; cross-compiles cleanly but not yet verified on a real Windows host.
