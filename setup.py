import os

from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup


def module_name(dirpath, filename):
    l = [os.path.splitext(filename)[0]]
    head = dirpath
    while True:
        head, tail = os.path.split(head)
        l.append(tail)
        if not head:
            break
    return '.'.join(reversed(l))


def get_extensions():
    extensions = [
        Extension('qurpc._kcp', ['src/kcp.c', 'src/ikcp.c'],
                  include_dirs=['src']),
    ]

    for dirpath, dirnames, filenames in os.walk('qurpc'):
        for filename in filenames:
            if filename.endswith('.pyx'):
                extensions.append(
                    Extension(module_name(dirpath, filename),
                              [os.path.join(dirpath, filename)]))

    return extensions


setup(packages=find_packages(),
      ext_modules=cythonize(get_extensions(), build_dir=f"build"))
