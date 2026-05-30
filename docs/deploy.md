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
- Build command: none, unless a future build step is explicitly added
- Runtime/backend: none required for the static site

## Before pushing to `main`

Run from the repository root:

```bash
rm -rf reports tools/__pycache__
python3 tools/audit_release_guard.py
git diff --check
git status --short
```

Do not push if the release guard fails.

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
python3 tools/audit_release_guard.py
git push
```

Do not force-push main.

## Build info

The site exposes a static build metadata file:

```text
/build-info.json
```

Before an important release, update it from the repository root:

```bash
python3 tools/update_build_info.py
```

If Render supports a build command, use:

```bash
python3 tools/update_build_info.py
```

This helps compare the live site with the Git commit that was intended for deploy.
