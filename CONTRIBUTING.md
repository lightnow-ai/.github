# Contributing to LightNow

This is the shared issue, pull request, and discussion standard for LightNow
repositories, including contributions created through MCP or coding agents.
Service READMEs and AGENTS.md files own component-specific development,
verification, and security requirements.

## Issues

Create an issue in the repository that owns the work. Choose Bug, Feature, or
Task and use the same short structure as the shared issue forms:

- **Problem or goal:** describe the problem and expected behavior or the intended
  outcome. Include impact when it helps prioritize the work.
- **Context:** provide reproduction steps and relevant evidence for bugs; add
  relevant examples or constraints for features/tasks. Link detailed evidence
  instead of pasting logs. Date observations when their freshness matters.
- **Acceptance criteria:** state a few testable outcomes that establish when the
  work is complete.

Use repository metadata for assignees and labels. Add scope, compatibility,
rollout, or security constraints only when they affect the work. Agent/MCP issue
creation must follow this structure explicitly; GitHub's web forms do not format
API-created issue bodies.

## Pull requests

Use the shared template for human and agent contributions:

- **Change:** explain the problem and resulting change in a few sentences.
- **Validation:** name relevant checks and observed results; link CI builds or
  detailed evidence. Distinguish completed checks from pending verification.
- **Related work:** link an existing issue when applicable. Use `Closes`, `Fixes`,
  or `Resolves` only when the PR completes that issue; omit this section when
  there is no related work. Do not create an issue solely to satisfy a template.

Mention risks, contract changes, migrations, or rollout requirements when they
matter. Update the description when scope or validation changes materially;
describe the final change without a chronological work log.

Dependency bots may retain their generated descriptions. All contributions must
still satisfy the repository's technical CI, security, and review requirements.
PR headings and issue links are authoring guidance, not GitHub status checks.

## Comments and reviews

- Comment for actionable review findings, questions, or decisions.
- Keep a blocker that requires a reviewer decision brief and link the evidence.
- Keep CI status and logs in checks/builds; do not add routine success, pending,
  or step-by-step progress comments.
- Keep coding-agent progress, MCP access diagnostics, and local worktree/runtime
  details in the agent chat. Do not publish `report_progress` output as PR comments.
- Update the PR description rather than appending repeated summaries. Resolve
  review threads when their findings have been addressed.

Never include credentials, customer data, or other sensitive information in
issues, PR descriptions, comments, or linked evidence.
