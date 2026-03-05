This kit features the following checks:

- License (GitHub API, whitelist: MIT|BSD-2-Clause|BSD-3-Clause)
- README presence + content checks
- Secrets (gitleaks; optional deep history via trufflehog)
- Issue/PR text scanning (basic secrets/internal refs)
- Dependencies: osv-scanner, pip-audit, npm audit
- SAST & Code quality: SonarCloud
- Linting: Prefer local linters (eslint/ruff/flake8…) → fallback to Super-Linter
- Tech stack (GitHub Languages API + manifest sniffers)
- Data file policy warnings
- AI usage detection (heuristic, informational)

Org prerequisites (once)

1. Create/confirm a SonarCloud organization linked to your GitHub org.

2. In GitHub Org Secrets, add:

- SONAR_TOKEN (SonarCloud user token with “Execute Analysis”)
- SONAR_ORGANIZATION (your SonarCloud org key, e.g. my-org)

3. To use the fan-out and make-public workflows, add:

- ORG_ADMIN_TOKEN (org-scoped PAT with repo, workflow; for make-public also needs repo admin on target repos).

Repos don’t need a sonar-project.properties. If a repo has one, the scan will use it; otherwise we pass minimal config.

## How teams adopt

1. In each repo, add a caller workflow:
   ```yaml
   # .github/workflows/compliance.yml
   name: Compliance
   on: [push, pull_request]
   schedule: [{ cron: "17 2 * * *" }]
   workflow_dispatch:
     inputs:
       history_depth:
         description: "Commits to scan for secrets (0 = off)"
         default: "0"
   permissions:
     contents: read
     security-events: write
   jobs:
     run:
       uses: your-org/compliance-kit/.github/workflows/repo-compliance.yml@main
       with:
         history_depth: ${{ github.event.inputs.history_depth || 0 }}
       secrets: inherit

2. Use Make Repository Public (Gated) instead of manually toggling visibility.

3. Run Org fan-out from this repo to sweep all repos.
