---
title: Update the search index
keywords: search, Algolia, search index, update search index
summary: "Build, validate, and publish the Hugo-generated Algolia search index."
permalink: docs-meta-search.html
aliases:
  - /docs-meta-search.html
---

## Overview

Hugo renders searchable page content to `public/algolia.json`. The Node.js CLI
in `tools/algolia-index.mjs` converts that export into Algolia records, validates
record sizes, configures index settings, and atomically replaces the index.

## Validate locally

Install dependencies, build the site, and run the dry validation:

```bash
npm ci
npm run test:algolia
hugo --gc --minify --cleanDestinationDir --environment production
npm run algolia:index -- --dry-run
```

The dry run does not contact Algolia. It validates the Hugo JSON schema,
configured content selector, generated records, and maximum record size.

## Publish an index

Use a restricted Algolia indexing key and export the application, key, and
index values in the current shell:

```bash
export ALGOLIA_APP_ID="your-application-id"
export ALGOLIA_WRITE_API_KEY="your-restricted-indexing-key"
export ALGOLIA_INDEX_NAME="your-index-name"
npm run algolia:index
```

The key needs `addObject`, `deleteIndex`, and `editSettings` permissions. Its
index restriction must also allow the temporary index prefix used for atomic
replacement.

Production updates run through the **Update the Algolia search index** workflow.
The workflow reads `ALGOLIA_APP_ID`, `ALGOLIA_WRITE_API_KEY`, and
`ALGOLIA_INDEX_NAME` from repository secrets.

See the repository's `docs/algolia.md` for complete personal-account setup and
sample query validation.
