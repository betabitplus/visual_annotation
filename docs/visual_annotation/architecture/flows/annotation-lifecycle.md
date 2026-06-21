---
name: annotation-lifecycle
doc_type: architecture
description: Runtime flow for one visual annotation request. Use when you need the request lifecycle.
---

# Annotation Lifecycle

## Overview

This document describes the runtime flow for one public annotation request.

Question this diagram answers: What happens between `annotate(...)` and the
returned image?

```mermaid
sequenceDiagram
    participant Caller
    participant Public as Public Facade
    participant Service as Runtime Service
    participant Handler as Slice Handler
    participant Drawing as Drawing Stack
    Caller->>Public: image + elements
    Public->>Service: validated request
    Service->>Handler: grouped elements
    Handler->>Drawing: detections
    Drawing-->>Caller: annotated response
```

## Main Flow

### Request Construction

- The public facade receives an image and iterable of elements.
- Public DTO construction validates image and element contracts.
- The facade delegates through the private root.

### Runtime Execution

- The service resolves the iterable into one trusted task.
- The annotator groups elements by concrete type.
- Each handler converts one group into supervision detections.

### Response

- Labeled detections receive a final label pass.
- The response carries the annotated image and `element_count`.

## Rules

- Keep public e2e scenarios shaped around this lifecycle.
- Keep runtime errors translated at the service boundary.
- Keep drawing dependencies private.
