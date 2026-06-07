Purpose
- Guidance for Copilot sessions working in this repository (MCDR plugins collection).

Build / install
- Install editable package and extras: python -m pip install -e .[mcdrpost,kill-server,minecraft-data-api]
- Install per-plugin deps (lightweight): python -m pip install -r src/MCDRpost/requirements.txt
- Use Python matching pyproject.toml: >=3.12 (pyproject) — some plugin READMEs mention 3.10+; prefer the pyproject setting.

Lint / typecheck
- Run mypy over the source: python -m mypy src/
- No repository-wide linters (flake8/black) configured; follow project style when adding tooling.

Tests
- This repository contains no formal test suite. No test runner configured.
- To check a single script or module, run it directly with python path/to/module.py or import it in a short REPL/test harness.

CI / workflows
- .github/workflows/pr-checks.yml enforces branch naming rules (only dev/* or hotfix/* can target master; feature/* must merge to dev/* first).
- .github/workflows/tag-dispatch.yml sends a repository_dispatch on tags.
- Check these workflows before changing branch/merge policies.

High-level architecture
- Monorepo of MCDReforged plugins under src/ (e.g., MCDRpost, KillServer, DevelopHandler).
- Each plugin is a self-contained Python package exposing PLUGIN_METADATA and an entrypoint (on_load / module-level registration). Plugins depend on MCDReforged (mcdreforged) and optional extras.
- MCDRpost is the largest plugin: modular, exposes an API (mcdrpost.api) for custom VersionHandlers and sound players, stores runtime data in config/ (config/MCDRpost/*), and provides migration tooling under src/MCDRpost-migration.
- dependencies/ contains third-party helpers (e.g., MCDataAPI) packaged alongside the plugins for convenience.

Key repository conventions
- Plugin metadata: Every plugin defines PLUGIN_METADATA with id, version, dependencies and other fields — Copilot should look for this when locating an entrypoint.
- Handler registration: Custom adapters follow register_handler(handler_class, checker_callable); the checker receives an Environment and must return bool.
- Config location: Plugins expect runtime configuration in config/<plugin_id>/ or paths defined in their README (MCDRpost uses config/MCDRpost/config.yml). Avoid hardcoding paths when adding features.
- Logging: Do not prepend manual plugin name prefixes to server.logger — MCDReforged already prepends [<plugin_id>]: per AGENTS.md notes.
- Language and docs: Chinese is the primary language for docs; English translations are kept alongside. Keep docs concise and mirror translations when editing.
- Branch rules: Follow dev/* and hotfix/* -> master policy. feature/* branches should be merged into dev/* first.
- Commit messages: repository prefers Conventional Commits (English or Simplified Chinese) and no emojis.

Existing AI assistant configs
- AGENTS.md exists — consult it for project-specific agent and documentation rules.
- Other assistant config files (CLAUDE.md, .cursorrules, etc.) are not present.

Where to look next
- pyproject.toml: dependency, mypy and extras configuration.
- src/MCDRpost/: main plugin, README and custom_handler.md (API docs).
- .github/workflows/: CI policies (branch checks, tag dispatch).
- dependencies/MCDataAPI/: bundled dependency docs.

If editing this file
- Keep guidance tightly scoped to repository mechanics, CI, and plugin conventions.
- Update the "Build / install" section if new CI or packaging steps are added.

Questions
- Want MCP server configurations added (Playwright, browsers, etc.)? Reply yes to configure relevant MCP servers.
