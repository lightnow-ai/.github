# LightNow

> One trusted MCP runtime across every AI client.

LightNow helps developers discover trusted MCP servers, manage one runtime
profile, and connect it to their AI clients through the LightNow Local Proxy.

Works with Codex, Claude Desktop, Claude Code, Cursor, VS Code, Antigravity,
Gemini CLI, and other MCP-compatible clients.

## Start in 30 seconds

```bash
brew tap lightnow-ai/tap
brew install lightnow-cli lightnow-proxy
lightnow login
lightnow sync --client codex --local-proxy
```

Restart your client after syncing. Replace `codex` with another supported
client, or follow the [quickstart](https://docs.lightnow.ai/getting-started/quickstart)
for alternative installation methods and configuration options.

## Explore LightNow

- [Website](https://lightnow.ai)
- [Documentation](https://docs.lightnow.ai)
- [LightNow CLI](https://github.com/lightnow-ai/lightnow-cli)
- [LightNow Local Proxy](https://github.com/lightnow-ai/lightnow-proxy)
- [Official MCP Registry](https://registry.modelcontextprotocol.io/)

The public LightNow CLI and LightNow Local Proxy components are licensed under
the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
