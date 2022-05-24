#!/usr/bin/env python

"""Tests for `uia` package."""

import uia

def test_package_publishes_version_info():
    """Tests that the `uia` publishes the current version"""

    assert hasattr(uia, '__version__')
