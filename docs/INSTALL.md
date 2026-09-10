# Installing Compileq

**Compileq is proprietary software from Psylinks Security Private Limited
(psylinkssecurity.com), distributed to licensed users directly (as a zip
or internal package registry) — not via public GitHub.** Replace the
git-clone steps below with however your organization distributes the
licensed copy internally.

## Option A — As a Claude Skill (Claude Code / Claude Cowork)

```bash
# obtain the licensed Compileq package from Psylinks Security Private Limited
cp -r compileq ~/.claude/skills/compileq   # or the project-local .claude/skills/ dir
pip install -r ~/.claude/skills/compileq/scanner/requirements.txt
```

Claude will pick up `SKILL.md` automatically and know when to invoke it —
just ask "scan this repo for compliance issues" or similar.

## Option B — As an MCP server (Cursor, VS Code + Copilot, Windsurf, Claude Desktop, etc.)

```bash
# obtain the licensed Compileq package from Psylinks Security Private Limited
cd compileq
pip install -r mcp_server/requirements.txt
```

Then add to your MCP host's config (example for a generic `mcp.json`-style
config — adjust the key names to your specific IDE's format):

```json
{
  "mcpServers": {
    "compileq": {
      "command": "python",
      "args": ["/absolute/path/to/compileq/mcp_server/server.py"]
    }
  }
}
```

- **Claude Desktop**: add this block to `claude_desktop_config.json` under
  `mcpServers`.
- **Cursor**: Settings → MCP → Add new MCP server, same command/args.
- **VS Code + Copilot / Windsurf**: add to your `mcp.json` in the same shape.

Restart the IDE, and the tools `scan_repo`, `scan_repo_markdown`,
`list_known_regulations`, `lookup_regulation`, `list_official_sources`,
`check_source_url`, and `draft_new_rule_stub` will be available for the AI
to call.

## Option C — CLI only, no AI host

```bash
pip install -r scanner/requirements.txt
python -m scanner.cli scan /path/to/repo --markets EU,US-CA --out report.md
```

Useful for CI pipelines — see `docs/ROADMAP.md` for the planned GitHub
Action wrapper.
