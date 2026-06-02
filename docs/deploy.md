# Deploy and Live QA

This project is a static bilingual site under `site/`.

## Production URL

Canonical live site:

```text
https://between-potential-and-ideal.onrender.com
```

## Expected deploy model

The live site should serve the committed contents of the `site/` directory from the `main` branch.

Expected Render settings:

- Source branch: `main`
- Public / publish directory: `site`
- Build command: optional. If enabled, use `python3 tools/update_build_info.py` so live `/build-info.json` reflects the deployed checkout.
- Runtime/backend: none required for the static site

## Before pushing to `main`

Run from the repository root:

```bash
rm -rf reports tools/__pycache__
python3 tools/final_release_qa.py --scan
git status --short
```

`tools/final_release_qa.py` wraps:

- `git diff --check`
- `tools/check_build_info_matches_head.py`
- `tools/audit_release_guard.py`

For diagnostic/local detailed guard runs, the direct command remains:

```bash
python3 tools/audit_release_guard.py
```

Do not push if the final release QA reports blockers.

Do not commit:

- `reports/`
- `tools/__pycache__/`
- temporary repair scripts
- local screenshots unless explicitly requested

## After pushing to `main`

Wait for Render to finish deploying, then test important live URLs:

```bash
python3 tools/check_live_deploy_urls.py
```

If the live site appears stale, verify all of the following before calling it a deployment blocker:

- Render deploy finished successfully.
- Correct branch is deployed.
- Hard refresh was performed.
- Incognito/private window was tested.
- Page source was checked, not only rendered DOM.
- Browser/CDN cache was considered.
- `/build-info.json` was checked on the live site.

If evidence is incomplete, record: `Deployment verification inconclusive`.

## Manual visual checks

Check:

- Hebrew pages are RTL and right-aligned.
- English pages are LTR and left-aligned.
- The files table looks unchanged visually after accessibility fixes.
- The story appendices still have 16 stories in the protected order.
- The two new stories appear in the correct positions.
- AI dialogue files show the AI disclosure near the top.
- No temporary repair notes or local report files appear on the live site.

## Emergency rollback

If live output is broken after a push:

```bash
git log --oneline --decorate -10
git revert <bad_commit_sha>
python3 tools/final_release_qa.py --scan
git push
```

Do not force-push main.

## Build info

The site exposes a static build metadata file:

```text
/build-info.json
```

A committed static JSON file cannot contain the SHA of the commit that contains itself, because the commit SHA is calculated from the tree including that file. The live Render build should regenerate this file during build if build commands are enabled.

Recommended Render build command when supported:

```bash
python3 tools/update_build_info.py
```

Local verification command:

```bash
python3 tools/check_build_info_matches_head.py
```

A build-info mismatch in the repository checkout is a warning unless live deployment evidence proves a stale deploy.
