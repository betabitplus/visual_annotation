---
name: visual-annotation-concepts
doc_type: index
description: Index of visual annotation concept docs. Use when you need the durable behavior slice model.
---

# Concepts

## Overview

These docs describe the stable behavior slices that docs, e2e tests, workbench
scripts, and CI matrix names mirror.

## Files

- [public-boundary-and-errors.md](public-boundary-and-errors.md)
  Explains the supported top-level public API and error translation model.
  Use it to guide changes to public exports or exception behavior.
- [box-annotation.md](box-annotation.md)
  Explains labeled box and page-box drawing.
  Use it to guide changes to bounding-box behavior.
- [point-annotation.md](point-annotation.md)
  Explains point drawing and `xy` adaptation.
  Use it to guide changes to point behavior.
- [mask-annotation.md](mask-annotation.md)
  Explains mask drawing and mask-to-box derivation.
  Use it to guide changes to mask behavior.
- [page-element-compatibility.md](page-element-compatibility.md)
  Explains screenshot/page element compatibility.
  Use it to guide changes to document-page annotation behavior.
- [configuration-and-validation.md](configuration-and-validation.md)
  Explains config snapshots and public validation defaults.
  Use it to guide changes to config or validation rules.
