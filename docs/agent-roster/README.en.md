# agent-roster

A capability for coding agents: **remember which coding agents are around and what each is good at, then delegate work on the basis of that evidence**.

Use it to ask Claude to plan, Codex to review, Kiro to implement — anything like that. The hard part is not how to launch them (the ACP ecosystem already solved that). The hard part is **what makes the choice justified**, and whether that justification gets more accurate with use.

## What it does

- **Roster**: register "which agent lives on which machine", recording version, availability, and disposition.
- **Routing**: when a task arrives, read the roster and past traces, pick the right match, and write down why before executing.
- **Delegation**: dispatch the task with read-only or writable permissions, collect the handoff, and land it in a caller-specified location.
- **Traces**: only kept when there is a lesson. Once enough same-kind evidence accumulates, a human confirms whether to promote the rule.

## What it does not do

- It does not implement the capabilities of the delegated agents themselves.
- It does not score or rank agents. See [ADR 0002](./docs/adr/0002-no-scoring-only-cases.md).
- v1 does **not** execute across machines. Remote endpoints can be registered, but dispatch only happens on the local machine. The data model is designed to support cross-machine dispatch later.
- It does not store any real data in this repository. See [ADR 0001](./docs/adr/0001-ledger-lives-outside-this-repo.md).

## Installation

```bash
npx skills add sunzhenkai/agent-roster -s agent-roster -g -y
```

Audit any externally sourced skill before installing it.

## Configuration

Data lives in the user's own private location — this repository does not assume where:

```yaml
# ~/.config/agent-roster/config.yaml
data_root: ~/path/to/your/private/data-repo
```

The roster and traces land under `<data_root>/agents/`. Format is described in
[endpoint-schema.md](./skills/agent-roster/references/endpoint-schema.md) and
[trace-format.md](./skills/agent-roster/references/trace-format.md).

## Probing what is on the local machine

```bash
python3 skills/agent-roster/scripts/probe_endpoints.py             # is it installed, which version
python3 skills/agent-roster/scripts/probe_endpoints.py --level 2   # confirm ACP adapter handshakes
python3 skills/agent-roster/scripts/probe_endpoints.py --render    # paste-ready status block
```

Standard Python 3 library only. Level 2 talks ACP directly to the adapter (JSON-RPC over stdio); no extra client required.

## Execution layer

The default executor is [acpx](https://acpx.sh) — a headless command-line client for ACP with built-in session management, permission policies, and structured event streams. The skill itself only depends on a thin adapter contract (endpoint + prompt + working directory + permission → structured result), so swapping executors is a matter of changing [delegation-contract.md](./skills/agent-roster/references/delegation-contract.md).

"Swapping executors" means switching to another equivalent implementation, and there is currently only one in this repo: a direct ACP fallback used when `acpx` is missing. The fallback only covers one-shot round-trips; sessions, timeouts, and permission tiers must be assembled ad hoc, so it is not a peer path. When `acpx` is not on `PATH`, delegation stops and the skill proposes installing it. Only an explicit user rejection can take the fallback path.

## Related documentation

- [CONTEXT.md](./CONTEXT.md): glossary. Read it first when you see Endpoint, Delegation, Trace, etc.
- [docs/adr/](./docs/adr/): key decisions and rejected alternatives.
- [SKILL.md](./skills/agent-roster/SKILL.md): the skill body.
- [README.md (中文)](./README.md): Simplified Chinese version.

## License

MIT
