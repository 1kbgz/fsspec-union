class TestFs:
    def test_fs_union(self, fs_union_importer):
        import my_local_file1
        import my_local_file2

        assert my_local_file1.foo1() == "This is a local file 1."
        assert my_local_file2.foo2() == "This is a local file 2."

        import masked

        assert masked.masked() == 1

    def test_fs_union_inverse(self, fs_union_importer_inverse):
        import my_local_file1
        import my_local_file2

        assert my_local_file1.foo1() == "This is a local file 1."
        assert my_local_file2.foo2() == "This is a local file 2."

        import masked

        assert masked.masked() == 2
