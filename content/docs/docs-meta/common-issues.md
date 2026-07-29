---
title: Troubleshooting and common issues
permalink: docs-meta-common-issues.html
aliases:
  - /docs-meta-common-issues.html
keywords: issues, troubleshooting, hugo, modules, build locally
summary: "Solutions for common local Hugo and module build problems."
---

## Hugo cannot download a module

Run `hugo mod verify` and confirm that Go can reach the module source. A fresh
clone needs network access the first time it downloads the versions recorded in
`go.mod`.

If an upstream repository rewrote a commit that was already published, the
recorded checksum may no longer match. Do not disable checksum verification as
a general workaround. Update the affected module to an immutable upstream
commit and commit the resulting `go.mod` and `go.sum` changes.

## Local content is older than upstream content

Hugo builds imported documentation from the revisions pinned in `go.mod`, not
from a separate local checkout. Run the **Update Hugo modules** workflow or:

```bash
python3 tools/sync_hugo_modules.py
```

Review and commit the resulting `go.mod` and `go.sum` changes.

## Hugo cannot clean its cache

The production command uses `--gc`, which requires a writable Hugo cache. Set a
cache directory owned by your user when building inside a restricted container:

```bash
HUGO_CACHEDIR=/tmp/precice-hugo-cache hugo --gc --minify
```

## Search results are stale

Building Hugo only creates `public/algolia.json`; it does not upload records.
Validate the export with `npm run algolia:index -- --dry-run`, then run the
**Update the Algolia search index** workflow with the configured production
credentials.
