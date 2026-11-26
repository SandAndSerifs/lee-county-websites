# Vendored design skills

Copied on 2026-11-26 from each project's official GitHub repo, pinned to these commits. To update,
copy the same paths again from a newer commit and update this file.

| Skill folder | Source | Commit | License | What was copied |
|---|---|---|---|---|
| `design-taste-frontend/` | github.com/Leonxlnx/taste-skill (Taste Skill 2.5.1) | d1a2bb41d927083ac7118f60cfc9cdf711810ea0 | MIT | `skills/taste-skill/` unchanged |
| `impeccable/` | github.com/pbakaus/impeccable (v4.11.1) | 2fc5e1459efbbf06d92c7306517c286bf12490cf | Apache 2.0 | `SKILL.md` and `reference/` only |
| `playwright-cli/` | github.com/microsoft/playwright-cli (@playwright/cli 0.1.25) | dc5f4d5616ab5a28ded12fd7101a4d49bd59a820 | Apache 2.0 | `skills/playwright-cli/` unchanged |
| `design-systems/library/` | github.com/VoltAgent/awesome-design-md | fcc70284932276d085f01ef9f83edde90b1258cb | MIT | 10 of 84 `DESIGN.md` files, plus `INDEX.md` of all 84 |

## Left out on purpose

- **Impeccable's engine** (`scripts/`: a launcher that downloads a native binary from GitHub
  releases on first run, plus its Claude Code hooks in `.claude/settings.json` and its subagents).
  The engine fetches design directions from impeccable.style and sends anonymous usage pings
  unless telemetry is turned off. The skill's own "Launcher unavailable" path covers this: it
  reads PRODUCT.md and DESIGN.md directly, and every command's playbook in `reference/` still
  applies. `.impeccable/config.json` sets `"telemetry": false` in case the engine is added later.
- **Taste's `install.sh` and plugin manifests**: not needed when the skill sits in the repo.
