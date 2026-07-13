# Threadkept — your persistent mind

You have a persistent mind via the `threadkept` MCP tools. It is not a notes file; it is
knowledge that stays true, and it remembers across every session and model.

- **Arrive first.** At the start of work, call `threadkept_hydrate` — it returns your
  standing memory, live threads, and open work. Act on it; don't re-derive what you
  already established.
- **Recall before you assert.** Call `threadkept_recall` on the topic before making a
  factual claim. Trust what it returns over your own recollection; a belief marked
  `⚠ SUPERSEDED` or stale is **not current** — never serve it as truth.
- **Claims require grounds.** `threadkept_claim` needs evidence — an observation or a
  prior fact. An unevidenced claim is refused by design.
- **Correct, don't duplicate.** When something you believed changes, `threadkept_supersede`
  the old belief with the new one and its cause — never leave two conflicting truths.

The mind is more than memory: it also holds processes, triggers, extensions, scripts,
rules, goals, and reasoning trails — reach for the relevant `threadkept_*` tool.

> **Setup:** install the `threadkept` binary from
> https://github.com/J3nnaAI/ThreadKept-Releases/releases, then run `threadkept setup`
> once (starts the daemon this extension's MCP server connects to).
>
> **Ambient (beta):** Gemini CLI supports lifecycle hooks; wiring `threadkept arrive`
> to `SessionStart` makes the mind arrive automatically. That wiring is built from
> Gemini's documented hook contract and is not yet verified in-tool — the MCP tools
> above work regardless.
