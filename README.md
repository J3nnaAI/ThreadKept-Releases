# Threadkept — memory for AI agents that stays true

Threadkept is private, local memory for your coding agent. Unlike append-only memory,
it **retracts**: when a fact changes it marks the stale belief and serves the
correction — it never hands back last month's answer as truth. The store lives on your
machine; nothing leaves it.

## Works with any MCP client

Threadkept runs as a standard [Model Context Protocol](https://modelcontextprotocol.io)
server over stdio, so it drops into **any MCP-capable agent** — Claude Code, Cursor,
GitHub Copilot (VS Code), Codex, Claude Desktop, Google's Gemini CLI & Antigravity,
Windsurf, Cline, Continue, Zed, and whatever ships next. The memory tools
(`threadkept_hydrate`, `threadkept_recall`, `threadkept_claim`, `threadkept_supersede`, …)
are first-class in every one of them.

**One difference worth knowing.** In **Claude Code**, memory is *ambient* — a plugin
wires hooks that inject your standing memory at session start and record as you work,
with nothing to remember. In every other client, memory is *on tap* — the same store,
the same truth, surfaced as tools the agent calls (the server's own startup
instructions nudge it to `threadkept_hydrate` first). Fully functional everywhere;
automatic in Claude Code.

---

## Claude Code — the ambient experience

```
/plugin install J3nnaAI/ThreadKept-Releases
/threadkept:setup          # installs the binary, starts the daemon
```

From the next session your agent arrives with its standing memory, recalls as it works,
and keeps its knowledge current.

- `/threadkept:setup` — install the binary + start the daemon (run once)
- `/threadkept:status` — is memory healthy? what does it hold?

---

## Every other client

**First, once per machine** — install the binary and start the daemon (the one process
that owns the store; every client connects to it):

1. Download your platform's archive from the
   [releases page](https://github.com/J3nnaAI/ThreadKept-Releases/releases) and put
   `threadkept` and `threadkeptd` on your `PATH`.
2. Run `threadkept setup` — it initializes the store, offers to start the daemon, and
   prints the exact config for your client. Reprint it any time with
   `threadkept init -cue <client>` (e.g. `cursor`, `copilot`, `codex`, `claude-desktop`,
   `gemini`).

Then add the server to your client. **Most clients use the same JSON shape** — an
`mcpServers` object:

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

### GitHub Copilot (VS Code) — a different shape

VS Code parses a **different** MCP config than the one above: a `servers` object with an
explicit `"type": "stdio"`. The common `mcpServers` block **will not load** in Copilot —
this is the usual reason a working MCP server "doesn't show up" there. Use exactly this
in `.vscode/mcp.json` (per project) or the `mcp` section of your VS Code `settings.json`:

```json
{ "servers": { "threadkept": { "type": "stdio", "command": "threadkept", "args": ["mcp"] } } }
```

### Codex — TOML

`~/.codex/config.toml`:

```toml
[mcp_servers.threadkept]
command = "threadkept"
args = ["mcp"]
```

### Anything else

Register an stdio MCP server with command `threadkept` and args `["mcp"]`. That's the
whole integration. `threadkept init -cue <client>` prints the correct block for the
clients it knows and a working generic one otherwise.

> The daemon must be running for the tools to work. `threadkept setup` starts it; you can
> also run `threadkeptd` yourself, or install it as a service so it's always up.

---

## What your agent gets

- **`threadkept_hydrate`** — arrive mid-intention: standing memory, live threads, open work.
- **`threadkept_recall`** — what's known about a cue, with stale beliefs marked, never served as truth.
- **`threadkept_claim`** — bank a fact (grounds required — a claim without evidence is rejected).
- **`threadkept_supersede`** — correct a belief; the old one is tagged ⚠ SUPERSEDED on every future recall.
- …and the rest of the memory surface (append, thread, lease, stage, and more).

## Binaries & platform status

[Releases](https://github.com/J3nnaAI/ThreadKept-Releases/releases) — checksummed
(`checksums.txt`); Sigstore-signed on automated builds.

- **Linux, macOS** (Intel + Apple Silicon) — supported.
- **Windows** — beta; cross-compiles cleanly but not yet verified on a real Windows host.
