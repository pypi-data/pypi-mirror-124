#!/usr/bin/env python3
# coding=utf-8
# Copyright (C) 2021 CORIA
"""Compile and install pyBOS."""
from subprocess import CalledProcessError, run

from setuptools import setup

try:
    run(["git", "branch"], check=True)
except (CalledProcessError, FileNotFoundError):
    setup()
else:
    # Add the version from git
    # --------------------------------
    setup(use_scm_version={"write_to": "pybos/version.py", "fallback_version": "0.0.0"})
