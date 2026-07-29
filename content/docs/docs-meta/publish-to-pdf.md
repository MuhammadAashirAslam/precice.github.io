---
title: Generate PDF documentation
permalink: docs-meta-publish-to-pdf.html
aliases:
  - /docs-meta-publish-to-pdf.html
keywords: pdf, publish to pdf, generate pdf
summary: "Status and scope of PDF generation for the Hugo documentation site."
---

## Current status

The website does not currently provide a supported full-document PDF pipeline.
The previous generator depended on the retired website build system and was
removed during the Hugo cutover.

Individual pages include print styles and can be printed or saved as PDF from a
browser. This is suitable for short extracts but does not assemble the complete
documentation or generate a global table of contents.

## Follow-up implementation

Full PDF generation is tracked separately from the website migration. The
intended direction is to select content with Hugo segments and convert the
result with an open-source HTML-to-PDF tool such as WeasyPrint. A production
implementation must define:

- the included sections and their order;
- stable internal links and page breaks;
- local availability of fonts, styles, diagrams, and equations;
- a reproducible CI build; and
- validation of the generated document.

Do not add a second website build system solely for PDF generation.
