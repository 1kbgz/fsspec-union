from __future__ import annotations

from fsspec import filesystem, get_filesystem_class
from fsspec.implementations.chained import ChainedFileSystem

__all__ = ("UnionFileSystem",)


class UnionFileSystem(ChainedFileSystem):
    """Union filesystem"""

    protocol: str = "union"

    def __init__(self, target_protocol=None, target_options=None, fs=None, **kwargs):
        """
        Args:
            target_protocol: str (optional) Target filesystem protocol. Provide either this or ``fs``.
            target_options: dict or None Passed to the instantiation of the FS, if fs is None.
            fs: filesystem instance The target filesystem to run against. Provide this or ``protocol``.
        """
        super().__init__(**kwargs)
        if fs is None and target_protocol is None:
            raise ValueError("Please provide filesystem instance(fs) or target_protocol")
        if not (fs is None) ^ (target_protocol is None):
            raise ValueError("Both filesystems (fs) and target_protocol may not be both given.")

        if target_protocol:
            # unpack the targets and then instantiate in reverse order
            fs_options = [{"target_protocol": target_protocol, "target_options": kwargs}]
            fss = []

            while "target_options" in target_options:
                target_protocol = target_options.pop("target_protocol")
                new_target_options = target_options.pop("target_options")
                kwargs = target_options
                fs_options.append({"target_protocol": target_protocol, "target_options": kwargs})
                target_options = new_target_options

            # instantiate in reverse order
            wrapped_fss = []
            for i, fspec in enumerate(reversed(fs_options)):
                target_protocol = fspec["target_protocol"]
                target_options = fspec["target_options"]

                fs_class = get_filesystem_class(target_protocol)
                if fs_class is None:
                    raise ValueError(f"Unknown filesystem protocol: {target_protocol}")
                if issubclass(fs_class, ChainedFileSystem) and fss:
                    target_options["fs"] = fss[-1]
                    wrapped_fss.append(fss[-1])
                fss.append(filesystem(target_protocol, **target_options))

            # remove wrapped filesystems
            fss = [fs for fs in fss if fs not in wrapped_fss]

            fss.reverse()
            self.fss = fss
            self.fs = fss[0]
        else:
            self.fss = [fs]
            self.fs = fs

    def exit(self):
        for fs in self.fss:
            if hasattr(fs, "exit"):
                fs.exit()

    def exists(self, path):
        for fs in self.fss:
            if fs.exists(path):
                return True
        return False

    def isfile(self, path):
        for fs in self.fss:
            if fs.exists(path):
                return fs.isfile(path)
        return False

    def isdir(self, path):
        for fs in self.fss:
            if fs.exists(path):
                return fs.isdir(path)
        return False

    def info(self, path, **kwargs):
        for fs in self.fss:
            if fs.exists(path):
                return fs.info(path, **kwargs)
        raise FileNotFoundError(f"File {path} not found in any of the union filesystems.")

    def open(self, path, mode="rb", **kwargs):
        if "w" in mode or "a" in mode or "+" in mode:
            # Open against first filesystem only
            return self.fss[0].open(path, mode=mode, **kwargs)
        for fs in self.fss:
            if fs.exists(path):
                return fs.open(path, mode=mode, **kwargs)
        raise FileNotFoundError(f"File {path} not found in any of the union filesystems.")

    @property
    def root(self):
        return ",".join(fs.root for fs in self.fss)

    def __getattribute__(self, item):
        if item in {
            "__class__",
            "__doc__",
            "__init__",
            "__module__",
            "__new__",
            "protocol",
            "fs",
            "fss",
            "root",
            # Implemented here
            "exists",
            "isfile",
            "isdir",
            "info",
            # python
            "exit",
        }:
            return object.__getattribute__(self, item)

        d = object.__getattribute__(self, "__dict__")
        fs = d.get("fs", None)
        fss = d.get("fss", [])

        # boolean attributes
        # evaluate until true, else give up
        if item in {
            "closed",
            "read_only",
            "writable",
            "readable",
            "seekable",
            "case_sensitive",
        }:
            raise NotImplementedError(f"Attribute {item} not implemented yet.")

        # For others, try and except
        for fs in fss:
            try:
                return getattr(fs, item)
            except AttributeError:
                continue

        # attributes of the superclass, while target is being set up
        return super().__getattribute__(item)
