#!/usr/bin/env python3
"""
Module POSTINSTALL -- Post-install script utilities
Sub-Package STDLIB of Package PLIB3
Copyright (C) 2008-2021 by Peter A. Donis

Released under the GNU General Public License, Version 2
See the LICENSE and README files for more information

This module contains utilities for obtaining information
about installed Python modules and packages and running
scripts that were installed with them.
"""

import os
import importlib
import runpy
import sysconfig

from plib.stdlib.builtins import first


def get_install_scheme(import_name):
    """Find the installation scheme for module or package ``import_name``.
    
    This allows appropriate directories to be determined for post-install scripts
    that write or symlink additional files.
    """
    
    mod = importlib.import_module(import_name)
    dirpath = os.path.dirname(mod.__file__)
    if hasattr(mod, '__path__'):
        # Back out of the package directories
        for _ in range(len(import_name.split('.'))):
            dirpath = os.path.dirname(dirpath)
    dirpath = os.path.normcase(dirpath)
    paths = [
        (scheme, os.path.normcase(sysconfig.get_path(key, scheme)))
        for key in ('purelib', 'platlib')
        for scheme in sysconfig.get_scheme_names()
    ]
    result = first(
        scheme for scheme, path in paths
        if (path == dirpath) and scheme.startswith(os.name)
    )
    if (result is None) and (os.name == 'posix'):
        # Allows posix-specific heuristics for cases where Python sysconfig info is borked
        # (e.g., Ubuntu)
        basepath = "/usr/local" if 'local' in dirpath else "/usr"
        result = (basepath,)
    return result


def get_bin_dir(import_name):
    """Return the corresponding ``bin`` directory for module or package ``import_name``.
    """
    scheme = get_install_scheme(import_name)
    if isinstance(scheme, tuple):
        dirpath = scheme[0]
        return os.path.join(dirpath, 'bin')
    return sysconfig.get_path('scripts', scheme)


def get_share_dir(name, import_name=None):
    """Return the corresponding ``share`` directory for module or package ``name``.
    
    The ``import_name`` parameter allows for modules or packages which are
    imported under a different name than the name they are given in your
    ``setup.py`` file.
    """
    scheme = get_install_scheme(import_name or name)
    if isinstance(scheme, tuple):
        dirpath = scheme[0]
        return os.path.join(dirpath, 'share', name)
    return os.path.join(
        sysconfig.get_path('data', scheme),
        'share',
        name
    )


def run_share_script(name, package_name, import_name=None, share_root=None, script_basename=None):
    script_dir = get_share_dir(package_name, import_name)
    if share_root:
        script_dir = os.path.join(script_dir, share_root)
    script_dir = os.path.join(script_dir, name)
    script_basename = script_basename or first(f for f in os.listdir(script_dir) if f.endswith('.py'))
    if not script_basename:
        raise RuntimeError("Script not found for {} in {}".format(name, script_dir))
    script_path = os.path.join(script_dir, script_basename)
    runpy.run_path(script_path, run_name='__main__')
