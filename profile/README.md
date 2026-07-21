![LightNow — one runtime for every AI client](https://raw.githubusercontent.com/lightnow-ai/.github/main/assets/profile/lightnow-hero.png)

**One trusted MCP runtime across every AI client.**

Discover trusted MCP servers, manage one runtime profile, and connect it to
Codex, Claude, Cursor, VS Code, Gemini CLI, Antigravity, and other MCP clients.

[![Get started](https://img.shields.io/badge/Get_started-06B6D4?style=for-the-badge&labelColor=083344)](https://docs.lightnow.ai/getting-started/quickstart)
[![Explore MCP servers](https://img.shields.io/badge/Explore_MCP_servers-0E7490?style=for-the-badge&labelColor=083344)](https://lightnow.ai/servers)
[![Read the docs](https://img.shields.io/badge/Read_the_docs-F59E0B?style=for-the-badge&labelColor=422006)](https://docs.lightnow.ai)

## Your MCP stack, without the sprawl

MCP configurations multiply quickly. LightNow turns them into one managed
runtime that stays consistent across every client and machine.

| 🔎 Discover | 🧭 Manage | ⚡ Connect |
| --- | --- | --- |
| Find MCP servers in a searchable public registry. | Choose profiles, secrets, and organization policy once. | Give every client one LightNow entry through the Local Proxy. |

## From zero to connected

Create a free [LightNow account](https://lightnow.ai), then connect your first
client:

```bash
brew tap lightnow-ai/tap
brew install lightnow-cli lightnow-proxy
lightnow login
lightnow sync --client codex --local-proxy
```

Restart your client after syncing. Replace `codex` with another supported
client, or follow the [quickstart](https://docs.lightnow.ai/getting-started/quickstart)
for alternative installation methods and configuration options.

## Built in the open

| Project | What it does |
| --- | --- |
| [**LightNow CLI**](https://github.com/lightnow-ai/lightnow-cli) | Sign in, discover MCP servers, and sync managed configurations to local clients. |
| [**LightNow Local Proxy**](https://github.com/lightnow-ai/lightnow-proxy) | Resolve profiles, secrets, and upstream MCP servers at runtime through one local entry. |

[Website](https://lightnow.ai) · [Quickstart](https://docs.lightnow.ai/getting-started/quickstart) · [Documentation](https://docs.lightnow.ai)
