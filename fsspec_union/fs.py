from __future__ import annotations

from fsspec import filesystem
from fsspec.implementations.chained import ChainedFileSystem

__all__ = ("UnionFileSystem",)


class UnionFileSystem(ChainedFileSystem):
    """Union filesystem"""

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
            for fspec in reversed(fs_options):
                target_protocol = fspec["target_protocol"]
                target_options = fspec["target_options"]
                fss.append(filesystem(target_protocol, fs=fss[-1] if fss else None, **target_options))
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
