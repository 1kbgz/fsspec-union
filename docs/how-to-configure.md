# How to configure union roots

Use `dir::` wrappers to give each backend a root with relative paths. Place the
highest-priority root first:

```python
from fsspec import url_to_fs

import fsspec_union

fs, _ = url_to_fs(
    "union::dir::file:///srv/overrides::dir::file:///srv/defaults"
)
try:
    metadata = fs.info("settings.json")
finally:
    fs.exit()
```

Install the required backend packages before substituting remote URLs. For
example, two S3 roots use:

```python
fs, _ = url_to_fs(
    "union::dir::s3://config-overrides::dir::s3://config-defaults"
)
try:
    present = fs.exists("settings.json")
finally:
    fs.exit()
```

Configure backend credentials through fsspec. Keep identical relative path
conventions across roots so precedence applies to the same logical names.

Use `exists`, `info`, `isfile`, and `isdir` for cross-root lookup. For an actual
read from a fallback root, open that root's filesystem directly; ordinary union
`open` currently delegates to the first backend. See [Method behavior](reference.md).
