---
name: status
description: Check whether the Threadkept memory daemon is running and healthy and report what the store holds.
---
# Threadkept status

Report the health of the operator's memory. Run `threadkept status` and relay it:
is the daemon up, how many memories are held, any durability fault. If the daemon is
down, say so plainly and offer to start it (`threadkeptd &`) — memory is not recording
until it is.
