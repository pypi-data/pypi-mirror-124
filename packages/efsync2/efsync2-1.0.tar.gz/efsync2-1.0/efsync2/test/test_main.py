import pytest
from efsync2.main import efsync

efsync_path = 'efsync2/test/efsync2.yaml'

def test_main():
    res = efsync(efsync_path)
    assert res == True
