# Ordered lookup and delegation

A union can make several storage roots look like one search space. Ordering
resolves collisions: a path in an earlier root takes precedence over the same
name in a later root. This is useful for configuration overrides and fallback
metadata.

## Lookup and I/O have separate implementations

The package implements existence and metadata lookup as a loop over its roots.
Once a path exists, its kind and metadata come from that first match. A directory
in an earlier root can therefore mask a file with the same name in a later root.

Other attributes are delegated to the first backend that exposes them. That
selection happens before the method receives a path, so it cannot choose a
backend based on whether a file exists. This explains why a successful `exists`
check does not guarantee an ordinary union `open` can read a later-root file.

## Search does not imply caching

Lookup does not copy a result into an earlier root. Changes to the backing
filesystems remain changes to those filesystems; the union has no separate
cache-population or invalidation policy. Directory listings are likewise delegated
rather than merged.

These limits matter when combining the union with an importer or another chained
filesystem: a consumer may discover a path through metadata lookup but fail when
it reads that path. The [reference](reference.md) describes the current method
boundary.
