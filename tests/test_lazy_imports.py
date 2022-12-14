import pytest
import sys

from lazy_imports import lazy_imports, ModuleNotAdded, ModuleAlreadyAdded, InvalidModule

@pytest.fixture(autouse=True)
def clear_cache():
    lazy_imports.clear()

def test_can_add_valid_module():
    lazy_imports.add_module("test_module_1")

    assert "test_module_1" not in sys.modules.keys()

def test_can_add_invalid_module():
    lazy_imports.add_module("not_existing_module")

def test_module_is_imported():
    lazy_imports.add_module("test_module_2")

    assert "test_module_2" not in sys.modules.keys()
    assert lazy_imports.test_module_2.a == 1
    assert "test_module_2" in sys.modules.keys()

def test_invalid_module_raises_when_used():
    lazy_imports.add_module("not_existing_module")

    with pytest.raises(InvalidModule):
        lazy_imports.not_existing_module

def test_raises_if_module_not_added():
    with pytest.raises(ModuleNotAdded):
        lazy_imports.not_existing_module

def test_cant_add_module_more_than_once():
    lazy_imports.add_module("test_module_3")

    with pytest.raises(ModuleAlreadyAdded):
        lazy_imports.add_module("test_module_3")
