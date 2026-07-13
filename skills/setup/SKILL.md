---
name: setup
description: Install the Threadkept memory binary, initialize the store, and start the daemon so this plugin's hooks and tools work. Run once after enabling the plugin.
---
# Threadkept setup

Get the Threadkept memory daemon running so this plugin's hooks and MCP tools work.

IMPORTANT: the plugin already wires the memory hooks. Do NOT run `threadkept setup` —
that writes a SECOND set of hooks into settings.json and they double-fire. This skill
only installs the binary, initializes the store, and starts the daemon.

1. Is it already installed? `threadkept --version` (or `which threadkept`).
2. If not: download the latest release for this OS/arch from
   https://github.com/J3nnaAI/ThreadKept-Releases/releases/latest — pick the archive
   matching your platform (e.g. `threadkept_<ver>_darwin_arm64.tar.gz`), verify it
   against `checksums.txt`, extract, and put `threadkept` and `threadkeptd` on PATH
   (e.g. `~/.local/bin`).
3. Initialize the store if absent: `threadkept init`.
4. Start the daemon if it isn't running: `threadkeptd &`, then confirm `threadkept status`.

Report the daemon status to the operator. Once it's up, memory is live — recall,
claims, supersession, and the arrival packet all work from here.
