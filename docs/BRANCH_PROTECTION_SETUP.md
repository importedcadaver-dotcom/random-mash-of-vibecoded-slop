# Protect `main` in this shared AI-game monorepo

**Status on 2026-11-09:** The connected GitHub integration returned `[]` for repository rulesets. Reading `main` branch-protection settings returned **403: Resource not accessible by integration**. That means the existing protection state could not be confirmed, and this agent **could not install GitHub-enforced protection** from the connection. This file is a handoff checklist, **not an enabled rule**.

Repository: `importedcadaver-dotcom/random-mash-of-vibecoded-slop` (public).

## Owner actions in GitHub

1. Open **Repository → Settings → Rules → Rulesets** (or the Rulesets option under Settings).
2. Choose **New branch ruleset** and name it `shared-monorepo-main-pr-gate`.
3. Set **Enforcement** to **Active** and target the repository's **default branch (`main`)**.
4. Turn on **Require a pull request before merging**; select **0 required approvals initially** if only one human owner is available (a required self-approval would otherwise block the maintainer). Add human peer approvals later when practical.
5. Enable **Block force pushes** and **Restrict deletions** (GitHub's wording may differ).
6. Keep the bypass list empty if practical. If an admin bypass is necessary, choose **PR-only bypass**, not unrestricted direct push, when offered.
7. **Do not require a specific global CI status check until an always-running repo-wide PR gate exists.** Current game CI uses `paths:` filters; a check that never starts for docs-only or another game's PR can permanently block merges. Once a lightweight always-on PR workflow is configured, require its actual observed unique job name. Game-specific test runs still need review.
8. Save, then confirm the ruleset is **Active** and test by opening a harmless PR (and, if safe, observing that direct push to `main` is rejected).
9. Record the ruleset URL/ID and verification date in a follow-up PR or issue. Never write "protected" based only on this document.

GitHub documentation:
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets

## Safety measures already in repo (process, not server enforcement)

- Root and game-specific `AGENTS.md` instructions.
- Parallel worktrees and scoped game folders, documented in `docs/MULTI_AGENT_WORKFLOW.md`.
- GitHub Actions Windows/Linux Pygame tests for Mud Pie Masters paths.
- Per-PR identity, ownership, and verification requirements.

## Always-on PR gate (implemented in this branch)

`.github/workflows/agent-governance.yml` and `.github/scripts/validate_agent_pr.py` run on every PR, check agent attribution, and detect accidental cross-game changes and common local files. After it runs successfully in GitHub Actions, note its exact check name (`agent-governance` job) and optionally require that status check in the ruleset. This gate is not enforced against `main` until branch protection is activated. Review `CODEOWNERS` only when real human maintainers are available; declaring a model name is not an authenticated GitHub CODEOWNER. Do not enable protection settings that accidentally block the sole maintainer with no reviewer.
