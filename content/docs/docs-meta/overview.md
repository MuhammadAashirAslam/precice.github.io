---
title: Documentation of the documentation
keywords: pages, authoring, frontmatter, hugo, modules
summary: "Learn how to preview, structure, and contribute to the preCICE documentation website built with Hugo."
permalink: docs-meta-overview.html
aliases:
  - /docs-meta-overview.html
---

## About the website

The preCICE website is built with [Hugo](https://gohugo.io/). Website-owned
pages live in `content/`, navigation data lives in `data/sidebars/`, and Hugo
templates live in `layouts/`. Documentation owned by tutorials, adapters, and
tools is included from those repositories with Hugo Modules.

See the [content guidelines](docs-meta-content-guidelines.html) for writing
style and accessibility guidance.

## Preview the website

Install Hugo Extended and Go using the versions listed in the repository
`README.md`, then run:

```bash
hugo server
```

Open <http://localhost:1313/>. Hugo watches local files and rebuilds the site
when they change. Module dependencies are downloaded automatically at the exact
versions recorded in `go.mod`.

Use the production build before opening a pull request:

```bash
hugo mod verify
hugo --gc --minify --cleanDestinationDir --environment production
```

## Add website content

Store a page below the section that owns it. For example:

```text
content/
└── docs/
    └── configuration/
        └── basics/
            └── introduction.md
```

Directories containing `_index.md` are Hugo sections. Section front matter can
define a `cascade` so child pages inherit the correct sidebar, layout, and table
of contents settings.

Minimal page front matter is:

```yaml
---
title: Configuration basics
summary: "Learn how to configure participants, meshes, data, and coupling schemes."
aliases:
  - /configuration-introduction.html
---
```

Use `aliases` to preserve an established URL when content moves. New pages
normally derive their URL from their path and do not need an explicit
`permalink`.

## Update navigation

Sidebar files are stored in `data/sidebars/`. Their `url` values should match
the rendered page URL and begin with `/`. The sidebar renderer supports nested
folders and automatically expands the branch containing the current page.

Tutorial navigation is generated together with tutorial module mounts. Do not
manually add a tutorial to only one of those locations; run the **Sync
tutorials** workflow or `tools/sync_tutorials.py` instead.

## Edit imported documentation

Imported content remains owned by its source repository. Use the edit link on a
rendered page to open the correct upstream file. The website maps those files
to Hugo content paths in `config/_default/module.toml`.

To add a new imported project:

1. Add its Go module path and Hugo mounts to `config/_default/module.toml`.
2. Run `hugo mod get github.com/precice/<repository>@<revision>`.
3. Run `hugo mod tidy` and `hugo mod verify`.
4. Add the resulting page URLs to the appropriate sidebar when needed.
5. Build the site and verify the source repository's edit links and Git dates.

The scheduled **Update Hugo modules** workflow checks upstream default branches
and updates `go.mod` and `go.sum`, so maintainers do not manually copy imported
files.

## Templates and shortcodes

Reusable page components are Hugo shortcodes in `layouts/shortcodes/`.
Navigation, metadata, and shared presentation belong in `layouts/partials/`.
See the [documentation cheatsheet](docs-meta-cheatsheet.html) for the supported
callouts and front matter fields.
