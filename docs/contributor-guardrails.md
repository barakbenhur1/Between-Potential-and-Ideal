# Contributor Guardrails

This project must be edited conservatively.

The goal is not redesign, not rewrite, not cleanup for its own sake, and not broad refactoring.

## Required workflow

1. Start from `main`.
2. Pull latest changes.
3. Make the smallest measurable change.
4. Run the repo-local final release QA command.
5. Review `git diff --check`.
6. Commit only intentional files.

## Before every commit

Run:

```bash
rm -rf reports tools/__pycache__
python3 tools/final_release_qa.py --scan
git diff --check
git status --short
```

`tools/final_release_qa.py` wraps the detailed `tools/audit_release_guard.py` gate.

## Never commit

- `reports/`
- `tools/__pycache__/`
- temporary repair scripts
- local screenshots
- downloaded ZIP extraction folders
- debug output files

## Do not change without explicit approval

- Story order
- Story IDs or slugs
- Public filenames
- Chapter images
- Story images
- Fonts
- Color palette
- Global spacing
- RTL/LTR direction rules
- CSS cleanup or consolidation
- HTML/PDF/DOCX/MD/TXT file variants

## Protected story rules

- Keep the appendix at 16 stories.
- Do not return the appendix to 14 stories.
- Do not move the two new stories out of their protected positions.
- Do not change the protected ending of the dog story: `ואז... הוא 🥱`.
- Do not turn `Three Queries` into a magical wish story.
- Do not add an explicit remaining-query counter to `Three Queries`.
- Do not soften `The Nauseating Truth`.
- Do not remove the creature mouths or fleshy stalks from `The Nauseating Truth`.

## AI rules

- Do not present AI as conscious.
- Do not present AI output as proof, authority, belief, memory, or living witness.
- Keep AI disclosure blocks in direct AI dialogue files.
- AI may be described as mirror, lens, stress test, or interpretive tool.

## Design and asset rules

- Do not delete images that look unused without an asset-reference audit.
- Do not replace images without explicit approval.
- Do not change image sizing or crop globally without visual QA.
- Do not perform CSS cleanup before the visual QA baseline is reviewed.
- Performance work must be measurable and reversible.

## Git rules

- Do not force-push `main`.
- Prefer `git revert` for rollback.
- Keep commits small and named by intent.
- Do not mix unrelated fixes in one commit.

## Acceptance criteria

A change is acceptable only when:

- Final release QA passes.
- `git diff --check` passes.
- `git status --short` contains only intentional files before commit.
- No protected content was changed accidentally.
- The visual output was checked when the change can affect layout.
