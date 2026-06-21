---
name: config-lifecycle
doc_type: architecture
description: Runtime flow for visual annotation config snapshots. Use when you need the config lifecycle.
---

# Config Lifecycle

## Overview

This document describes how config defaults become handler runtime state.

Question this diagram answers: How does appearance config reach supervision?

```mermaid
sequenceDiagram
    participant Defaults
    participant Config as AnnotatorConfig
    participant Install as Installed Snapshot
    participant Factory as Handler Factory
    Defaults->>Config: default values
    Config->>Install: explicit install
    Install->>Factory: frozen snapshot
    Factory->>Factory: configured annotators
```

## Main Flow

### Construction

- `AnnotatorConfig` starts from Python defaults.
- Color strings are normalized to `supervision.Color`.
- Numeric values are validated before the object is stored.

### Installation

- `install_config(...)` stores a frozen process snapshot.
- Installing config clears cached runtime services.
- Direct `annotate(..., config=...)` uses the supplied snapshot for one call.

## Rules

- Do not read mutable config state during handler execution.
- Keep config installation explicit.
- Keep old YAML ranges beside Python default constants.
