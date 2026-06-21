# visual_annotation

Standalone visual annotation helpers extracted from the researcher project.

The supported public entrypoint is the top-level `visual_annotation` package.
Call `annotate(...)` with a PIL image and visual elements such as boxes, points,
masks, or page elements, then receive an `AnnotationResponse` with an annotated
image and public metadata.

```python
from PIL import Image

from visual_annotation import VisualBox, annotate

image = Image.open("page.png").convert("RGB")
response = annotate(
    image,
    [VisualBox(label="car", coord=[0.19, 0.54, 0.32, 0.72])],
)
response.response_data.save("annotated.png")
```

## Development

```bash
direnv allow
direnv exec . uv sync --group dev --frozen
direnv exec . uv run pytest
```

Docs start at [docs/visual_annotation/README.md](docs/visual_annotation/README.md).
Manual dependency probes live under `workbench/visual_annotation/`.
