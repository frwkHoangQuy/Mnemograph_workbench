# Copilot Workflow Runbook

## A. Purpose and authority

This is a non-normative operational runbook.

Baseline documents, accepted ADRs and human-approved tasks take precedence over this workflow.

## B. Delivery surfaces

- VS Code Copilot Chat/Agent Mode is primary.
- Copilot CLI is secondary for terminal-heavy and controlled automation.
- Autopilot remains deferred.
- Models are not pinned in repository prompt or agent files.
- The SA reviewer recommends the lowest-cost capable model with each task prompt.

## C. Required workflow

1. Create or approve a bounded implementation issue.
2. Run /plan-from-issue read-only.
3. Human/SA reviews and approves the plan.
4. Select the appropriate development agent or use /implement-plan.
5. Implement exactly one approved small batch.
6. Run focused validation and the full quality gate.
7. Run independent test/security or /review-diff review.
8. Human reviews the diff.
9. Human creates the commit and pushes the branch.
10. Provide repository, branch and SHA to the independent SA reviewer.
11. Do not start the next batch until that review is approved or its amendment has been completed.

## D. Model-cost guidance

Prefer a small capable model for deterministic Markdown, YAML and narrow configuration work.

Use a coding-specialized model for multi-file code implementation, refactoring or debugging.

Use a stronger reasoning model only when architecture ambiguity or complex planning justifies its cost.

Never let automatic model selection silently broaden task scope.

## E. Pre-edit checks

Run these commands before editing:

- `git rev-parse HEAD`
- `git branch --show-current`
- `git status --porcelain=v2`

Stop if the starting SHA is wrong or unrelated changes exist.

## F. Validation commands

Run exactly these commands:

- `pnpm install --frozen-lockfile`
- `uv sync --all-packages --locked`
- `pnpm run validate`
- `docker compose -f infra/compose/docker-compose.yml config`
- `git diff --check`

Run the Compose validation only when Compose files, images, ports or initialization SQL change.

## G. Human-controlled Git

- Copilot does not commit, push, merge, amend or open a PR autonomously.
- Reviewed commits are not amended.
- Corrections use a separate reviewable follow-up commit.
- No destructive reset, restore, clean or stash without explicit human direction.
- Dirty working trees are diagnosed read-only before correction.

## H. VS Code customization diagnostics

Use Chat: Open Customizations to inspect repository instructions, agent files and prompt files.

Use the agents picker to switch between the repository development agents.

Use slash prompts for the repository prompt files when selecting the corresponding task.

Use Chat diagnostics and debug logs when a customization appears to be ignored or parsed incorrectly.

Expected repository customizations:

- 8 development custom agents
- 5 path-specific instructions
- 5 prompt files

## I. Stop conditions

- Normative ambiguity.
- Missing human approval.
- Dependency change without approval.
- Unrelated working-tree changes.
- Baseline mutation.
- Security or secret exposure.
- Destructive migration uncertainty.
- Validation failure.
- Scope or phase drift.

## J. Handoff record

For every checkpoint record:

- repository
- branch
- starting SHA
- resulting SHA
- prompt or model recommendation
- changed files
- validation result
- known manual checks
- reviewer decision
