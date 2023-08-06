#!/usr/bin/env python3
'''Dummy regression test to set up CI workflow.'''


import pytest


_TOLERANCE = 1.0e-10


def test_dummy():
    '''Dummy regression test to set up CI workflow.'''

    assert True


if __name__ == '__main__':
    pytest.main()
