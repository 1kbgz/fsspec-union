class TestFs:
    def test_fs_union(self, fs_union):
        assert fs_union.exists("my_local_file1.py")
        assert fs_union.exists("my_local_file2.py")
        content = fs_union.open("masked.py", "r").read()
        assert "return 1" in content

    def test_fs_import(self, fs_union_importer):
        import my_local_file1
        import my_local_file2

        assert my_local_file1.foo1() == "This is a local file 1."
        assert my_local_file2.foo2() == "This is a local file 2."

        import masked

        assert masked.masked() == 1

    def test_fs_union_inverse(self, fs_union_inverse):
        assert fs_union_inverse.exists("my_local_file1.py")
        assert fs_union_inverse.exists("my_local_file2.py")
        content = fs_union_inverse.open("masked.py", "r").read()
        assert "return 2" in content

    def test_fs_import_inverse(self, fs_union_importer_inverse):
        import my_local_file1
        import my_local_file2

        assert my_local_file1.foo1() == "This is a local file 1."
        assert my_local_file2.foo2() == "This is a local file 2."

        import masked

        assert masked.masked() == 2
