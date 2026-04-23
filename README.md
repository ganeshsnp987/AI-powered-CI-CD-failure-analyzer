# AI-Powered CI/CD Failure Analyzer

Automatically analyzes GitHub Actions failures using Claude and posts a root-cause diagnosis as a PR comment.

## Setup

1. Add `ANTHROPIC_API_KEY` to your repo's **Settings → Secrets and variables → Actions**
2. Push both workflows — `main.yml` (your CI) and `analyze-failure.yml` (the bot)

## How it works

1. A PR triggers `CI Pipeline` (`main.yml`) — runs your tests
2. If it fails, `workflow_run` fires `analyze-failure.yml`
3. The bot fetches the raw failure log via GitHub API
4. Sends it to Claude with a structured prompt
5. Posts the analysis as a PR comment (or job summary if no PR is found)

## Secrets required

| Secret | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `GITHUB_TOKEN` | Auto-provided by GitHub Actions |

## Sample output

> **Root cause:** `test_addition` failed because `add()` subtracts instead of adds.  
> **Failed step:** Run tests  
> **Fix:** Change `return a - b` to `return a + b` in `tests/test_app.py`  
> **Prevention:** Add a type-check lint rule or property-based tests for arithmetic helpers.
