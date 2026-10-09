# LightNow organization defaults

Shared contribution guidance and issue/PR templates for LightNow repositories
live here. See [CONTRIBUTING.md](CONTRIBUTING.md).

GitHub inherits these defaults when a repository has no corresponding local
file. A local `ISSUE_TEMPLATE` directory overrides all shared issue templates,
including `config.yml`; keep service-specific development instructions in the
service README or AGENTS.md instead of copying these templates.

This repository must be public for GitHub to apply organization defaults,
including to private service repositories. Defaults become active after merging
to `main`; removing local overrides enables inheritance in existing services.

Templates guide authors. Jenkins and relevant test/security checks provide
technical validation; no workflow checks PR headings or requires an issue link.

References: [GitHub organization defaults](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).
