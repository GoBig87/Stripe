#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages, Extension

from copy import deepcopy
from os.path import dirname, join, sep
from os import environ

def read(file_path):
    with open(file_path) as fp:
        return fp.read()

def determine_base_flags():
    flags = {
        'libraries': ['libStripe'],
        'include_dirs': [join(src_path, 'dist','Frameworks','Stripe.framework','Headers')],
        'library_dirs': [],
        'extra_link_args': [],
        'extra_compile_args': []}

    sysroot = environ.get('IOSSDKROOT', environ.get('SDKROOT'))
    if not sysroot:
        raise Exception('IOSSDKROOT is not set')
    flags['include_dirs'] += [sysroot]
    flags['extra_compile_args'] += ['-isysroot', sysroot]
    flags['extra_link_args'] += ['-isysroot', sysroot]

    return flags

def merge(d1, *args):
    d1 = deepcopy(d1)
    for d2 in args:
        for key, value in d2.items():
            value = deepcopy(value)
            if key in d1:
                d1[key].extend(value)
            else:
                d1[key] = value
    return d1

def expand(root, *args):
    return join(root, *args)

class CythonExtension(Extension):

    def __init__(self, *args, **kwargs):
        Extension.__init__(self, *args, **kwargs)
        self.cython_directives = {
            'c_string_encoding': 'utf-8',
            'profile': 'USE_PROFILE' in environ,
            'embedsignature': 'USE_EMBEDSIGNATURE' in environ}
        # XXX with pip, setuptools is imported before distutils, and change
        # our pyx to c, then, cythonize doesn't happen. So force again our
        # sources
        self.sources = args[1]

def get_extensions_from_sources(sources):
    ext_modules = []
    for pyx, flags in sources.items():
        pyx = expand(src_path,pyx)
        depends = [expand(src_path, x) for x in flags.pop('depends', [])]
        f_depends = [x for x in depends if x.rsplit('.', 1)[-1] in ('m')]
        c_depends = [expand(src_path, x) for x in flags.pop('c_depends', [])]
        module_name = 'stripe'
        flags_clean = {'depends': depends}
        for key, value in flags.items():
            if len(value):
                flags_clean[key] = value
        ext_modules.append(CythonExtension(
            module_name, [pyx] + f_depends + c_depends, **flags_clean))
    return ext_modules

sources = {}
src_path = build_path = dirname(__file__)
base_flags = determine_base_flags()
osx_flags = {
    'extra_link_args': ['-framework', 'Stripe'],
    'extra_compile_args': ['-ObjC++'],
    'depends': ['stripe_c.m']}
sources['stripe.pyx'] = merge(base_flags, osx_flags)

ext_modules = get_extensions_from_sources(sources)

setup(
      name='stripe',
      version='0.1',
      description="A simple stripe ios wrapper",
      classifiers=[
                   'Development Status :: 1 - Development',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: iOS',
                   'Programming Language :: Objective-C',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Payment Processing',
                   ],
      keywords=['stripe', 'payment processing'],
      author='GoBig87',
      author_email='add_later@add)later.com',
      url='https://github.com/GoBig87/Stripe_iOS_Wrapper',
      license='BSD',
      packages=find_packages(where='.', exclude=['docs', 'tests']),
      ext_modules=ext_modules,
      include_package_data=True,
      zip_safe=False,
      setup_requires=[
                      'setuptools',
                      ],
      
      )

