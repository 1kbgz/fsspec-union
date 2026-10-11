from fsspec_union.fs import UnionFileSystem


class TestFs:
    def test_fs_union(self, fs_union):
        assert fs_union.exists("my_local_file1.py")
        assert fs_union.exists("my_local_file2.py")
        content = fs_union.open("masked.py", "r").read()
        assert "return 1" in content

    def test_fs_import(self, fs_union_importer):
        import my_local_file1  # ty: ignore[unresolved-import]  # Module provided by the filesystem import fixture.
        import my_local_file2  # ty: ignore[unresolved-import]  # Module provided by the filesystem import fixture.

        assert my_local_file1.foo1() == "This is a local file 1."
        assert my_local_file2.foo2() == "This is a local file 2."

        import masked  # ty: ignore[unresolved-import]  # Module provided by the filesystem import fixture.

        assert masked.masked() == 1

    def test_fs_union_inverse(self, fs_union_inverse):
        assert fs_union_inverse.exists("my_local_file1.py")
        assert fs_union_inverse.exists("my_local_file2.py")
        content = fs_union_inverse.open("masked.py", "r").read()
        assert "return 2" in content

    def test_fs_import_inverse(self, fs_union_importer_inverse):
        import my_local_file1  # ty: ignore[unresolved-import]  # Module provided by the filesystem import fixture.
        import my_local_file2  # ty: ignore[unresolved-import]  # Module provided by the filesystem import fixture.

        assert my_local_file1.foo1() == "This is a local file 1."
        assert my_local_file2.foo2() == "This is a local file 2."

        import masked  # ty: ignore[unresolved-import]  # Module provided by the filesystem import fixture.

        assert masked.masked() == 2

    def test_protocol_without_options(self):
        fs = UnionFileSystem(target_protocol="memory")
        assert fs.fs.protocol == "memory"

    def test_open_forwards_base_arguments(self):
        from unittest.mock import MagicMock

        target = MagicMock()
        union = UnionFileSystem(fs=target)
        UnionFileSystem.open(union, "data", "wb", 1024, {"maxblocks": 2}, "gzip", custom=True)
        target.open.assert_called_once_with("data", mode="wb", block_size=1024, cache_options={"maxblocks": 2}, compression="gzip", custom=True)
        UnionFileSystem.exists(union, "data", detail=True)
        target.exists.assert_called_once_with("data", detail=True)
