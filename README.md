# Stats Agent Toolkit

This 15-133 project builds on my HW6 [StatsHelper](https://github.com/guptaveer00/StatsHelper), a command-line app that finds statistics textbook passages from everyday questions. The toolkit lets Codex search the same local textbook index and gives a separate Codex session a procedure for checking a study guide against its sources.

## What the toolkit does

- **`search_stats_passages`** is the single tool on a local Python MCP server. It takes a question and returns up to five textbook passages with their result IDs, PDF page numbers, and cosine distances. Smaller distances mean closer matches. The search excludes personal notes.
- **`check-study-guide`** is a read-only skill for reviewing an existing statistics guide or recall answers when asked to check their sources. Give the reviewer the draft and the saved MCP response in a fresh session. It marks each claim as supported, partial, or unsupported and reports the evidence without editing the draft.

## Why I built it

In HW6 I wrote, “The expected passage is missing from the top five.” The MCP tool makes those ranked passages and their page references available directly to Codex so it can inspect what the index returned.

In HW7, while checking the unfinished Pocket Shuffle starter, I wrote, “Report what you actually verified and any limitations; don’t claim unfinished features work.” In HW6 I also wrote, “Do not call a test successful just because the app returned something.” I used the same idea for the checker. A relevant-looking search hit earns a supported verdict only when the cited text backs the claim.

## Installation

Use Python 3.13, the version tested on macOS. First build the local `study_v2` index using the setup steps in the [StatsHelper README](https://github.com/guptaveer00/StatsHelper#start-the-app). The server argument points to the directory containing `chroma_store/` and the `.model_cache/` used by StatsHelper. You can point it at a local copy of those directories, as I did for the demo.

From the toolkit directory, install the server dependencies.

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The skill is already in `.agents/skills/check-study-guide/`. Open the toolkit directory as your Codex workspace, or copy that whole skill folder into another project's `.agents/skills/`. In a fresh reviewer session, ask Codex to use `$check-study-guide` on a draft and its saved MCP results.

Add this block to the Codex `~/.codex/config.toml`. Replace all three absolute paths with paths on your machine. Restart the Codex session after saving.

```toml
[mcp_servers.stats]
command = "/ABSOLUTE/PATH/StatsAgentToolkit/.venv/bin/python"
args = ["/ABSOLUTE/PATH/StatsAgentToolkit/server.py", "/ABSOLUTE/PATH/StatsHelper"]
default_tools_approval_mode = "writes"
```

Ask Codex to call `search_stats_passages` for a statistics question and inspect the tool-call event for returned pages. I verified discovery and live calls in **Codex CLI on macOS**, using the same settings as command-line overrides. I also tested tool listing and calls through the Python MCP client's stdio transport. The VS Code extension was not tested.

## Sources and AI use

The assignment’s `spec-check` example uses a report-only review and an evidence requirement. This checker applies those ideas to source citations and uses no bundled scripts. The MCP server adapts the assignment's FastMCP stdio example and reuses the collection, metadata, and embedding model from my HW6 project. The textbook source is Larry Wasserman's *All of Statistics*. The repo distributes code and instructions. The textbook, local database, model cache, and full transcript stay local.

I used OpenAI Codex to help design and implement the toolkit, run independent author and reviewer sessions, revise the checker from the observed results, and draft the documentation. See [DEMONSTRATION.md](DEMONSTRATION.md) for the run excerpts and [ITERATION.md](ITERATION.md) for the before and after.

- [OpenAI documentation for Codex MCP registration](https://developers.openai.com/codex/mcp)
- [OpenAI documentation for Codex skills](https://developers.openai.com/codex/skills)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
