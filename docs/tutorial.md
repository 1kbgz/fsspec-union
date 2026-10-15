# Look up files in two directories

We will create two local directories and check their combined path metadata.

## Install

Use Python 3.11 or newer:

```console
python -m pip install fsspec-union
```

## Create two roots

Create `union_demo.py`:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from fsspec import url_to_fs

import fsspec_union

with TemporaryDirectory() as directory:
    first = Path(directory, "first")
    second = Path(directory, "second")
    first.mkdir()
    second.mkdir()
    (first / "shared.txt").write_bytes(b"first")
    (second / "shared.txt").write_bytes(b"second")
    (second / "extra.txt").write_bytes(b"extra")
```

## Resolve a union

Append inside the temporary-directory block:

```python
    url = f"union::dir::{first.as_uri()}::dir::{second.as_uri()}"
    fs, _ = url_to_fs(url)
    try:
        print(fs.exists("shared.txt"))
        print(fs.exists("extra.txt"))
        print(fs.exists("missing.txt"))
        print(fs.info("shared.txt")["size"])
    finally:
        fs.exit()
```

Run `python union_demo.py`:

```text
True
True
False
5
```

Both roots participate in existence lookup. The shared name has size 5, matching
`first`, because the first root wins.

## Reverse precedence

Replace the URL assignment with:

```python
    url = f"union::dir::{second.as_uri()}::dir::{first.as_uri()}"
```

Run the script again. The last line is now `6`, the size of `second`.

See the [reference](reference.md) before using read or write methods: metadata
lookup and delegated I/O currently have different coverage.
