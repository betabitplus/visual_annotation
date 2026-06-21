---
name: page-element-compatibility
doc_type: architecture
description: High-level explanation of page element compatibility. Use when you need the screenshot/page-box behavior model.
---

# Page Element Compatibility

## Overview

This document describes how document-page elements remain annotatable through
the same public package boundary as visual elements.

Question this diagram answers: How do page elements reuse visual annotation?

```mermaid
flowchart LR
    Page["PageElement"] --> Box["Box Slice"]
    Box --> Draw["Unlabeled Box"]
    Draw --> Response["Annotated Response"]
```

## Main Model

### Compatibility Shape

- Page elements carry a `coord` bounding box and `content` text.
- The content is preserved in the DTO but does not become a visual label.
- The response contract remains the same as other annotation calls.

### Verification Shape

- Public e2e coverage imports only `visual_annotation`.
- The scenario mirrors screenshot/quote-capture usage without importing old
  browser tooling.

## Rules

- Keep page elements public because upstream workflows pass them directly.
- Do not create a separate page-element runtime branch when box handling is enough.
- Keep e2e proof under `page_element_compatibility`.
