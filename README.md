# fsspec-union

Union handling for fsspec filesystems

[![Build Status](https://github.com/1kbgz/fsspec-union/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/1kbgz/fsspec-union/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/1kbgz/fsspec-union/branch/main/graph/badge.svg)](https://codecov.io/gh/1kbgz/fsspec-union)
[![License](https://img.shields.io/github/license/1kbgz/fsspec-union)](https://github.com/1kbgz/fsspec-union)
[![PyPI](https://img.shields.io/pypi/v/fsspec-union.svg)](https://pypi.python.org/pypi/fsspec-union)

## Overview

This library allows for efficient layering of [fsspec filesystems](https://github.com/fsspec/filesystem_spec) as a read-through cache via a chained fsspec filesystem `union::`.

Layer two paths, reading and writing files from/to the first satisfying location in `/path/one`, `/path/two`.

```python
fs = open("union::dir::file:///path/one/::dir::file:///path/two/")
```

Importing Python modules from the first satisfying S3 location, via [fsspec-python](https://github.com/1kbgz/fsspec-python):

```python
fs = open("python::union::s3://module/set/one::s3://module/set/two)

import module_from_set_one
import module_from_set_two
import shared_module # reads from s3://module/set/one
```

[![](https://raw.githubusercontent.com/1kbgz/fsspec-union/refs/heads/main/docs/img/yt.png)](https://youtu.be/M9o9SF5-Pzw?t=824)

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
