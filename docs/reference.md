# Union filesystem reference

## `UnionFileSystem`

Exported from `fsspec_union`; registered under the `union` protocol by its package
entry point.

```python
UnionFileSystem(target_protocol=None, target_options=None, fs=None, **kwargs)
```

Exactly one of `target_protocol` and `fs` is required. Invalid combinations raise
`ValueError`. `fs` supplies one existing backend. Chained URL construction uses
nested `target_protocol` and `target_options` to construct the ordered backends.
Chained wrappers remain attached to the backends they wrap.

| Attribute | Value                                                                 |
| --------- | --------------------------------------------------------------------- |
| `fss`     | Ordered list of constructed backends.                                 |
| `fs`      | First backend.                                                        |
| `root`    | Comma-joined backend roots; requires those backends to expose `root`. |

## Method behavior

| Operation                                                | Current behavior                                                                                        |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `exists(path)`                                           | True if any backend reports the path exists.                                                            |
| `isfile(path)`, `isdir(path)`                            | Kind from the first backend where the path exists.                                                      |
| `info(path, **kwargs)`                                   | Metadata from the first matching backend; missing paths raise `FileNotFoundError`.                      |
| `exit()`                                                 | Calls `exit()` on each backend that provides it.                                                        |
| `ls`, `open`, `cat_file`, and other delegated attributes | First backend that exposes the attribute. Calls do not retry later backends after a missing-file error. |

Although the class defines a cross-root `open` method, ordinary instance access
is intercepted by `__getattribute__` and delegated to a backend. It does not reach
that method. Reads from later roots and merged directory listings are therefore
not supported by ordinary delegated calls.

Access to `closed`, `read_only`, `writable`, `readable`, `seekable`, and
`case_sensitive` raises `NotImplementedError`. Writes through delegated methods
follow the selected backend's behavior. The implementation does not populate a
cache, copy files between roots, or provide copy-on-write semantics.
