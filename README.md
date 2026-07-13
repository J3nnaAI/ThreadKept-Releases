# Threadkept — memory for AI agents that stays true

Threadkept is private, local memory for your coding agent. Unlike append-only memory,
it **retracts**: when a fact changes, it marks the stale belief and serves the
correction — it never hands back last month's answer as truth. The store lives on your
machine; nothing leaves it.

## Install

```
/plugin install J3nnaAI/ThreadKept-Releases
/threadkept:setup          # installs the binary, starts the daemon
```

That's it. From the next session your agent arrives with its standing memory, recalls
as it works, and keeps its knowledge current.

- `/threadkept:setup` — install the binary + start the daemon (run once)
- `/threadkept:status` — is memory healthy? what does it hold?

Binaries: https://github.com/J3nnaAI/ThreadKept-Releases/releases — signed, checksummed.
macOS/Linux supported; Windows beta (pending verification).
