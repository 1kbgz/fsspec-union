import importlib
import sys
from pathlib import Path

import pytest
from fsspec import url_to_fs


@pytest.fixture(scope="function")
def fs_union():
    fs, _ = url_to_fs(f"union::dir::file://{Path(__file__).parent}/local1::dir::file://{Path(__file__).parent}/local2")
    yield fs


@pytest.fixture(scope="function")
def fs_union_importer():
    sys_meta_path_length = len(sys.meta_path)
    fs, _ = url_to_fs(f"python::union::dir::file://{Path(__file__).parent}/local1::dir::file://{Path(__file__).parent}/local2")
    import masked

    importlib.reload(masked)
    yield fs
    fs.exit()
    sys.modules.pop("masked", None)
    assert len(sys.meta_path) == sys_meta_path_length


@pytest.fixture(scope="function")
def fs_union_inverse():
    fs, _ = url_to_fs(f"union::dir::file://{Path(__file__).parent}/local2::dir::file://{Path(__file__).parent}/local1")
    yield fs


@pytest.fixture(scope="function")
def fs_union_importer_inverse():
    sys_meta_path_length = len(sys.meta_path)
    fs, _ = url_to_fs(f"python::union::dir::file://{Path(__file__).parent}/local2::dir::file://{Path(__file__).parent}/local1")
    import masked

    importlib.reload(masked)
    yield fs
    fs.exit()
    sys.modules.pop("masked", None)
    assert len(sys.meta_path) == sys_meta_path_length
