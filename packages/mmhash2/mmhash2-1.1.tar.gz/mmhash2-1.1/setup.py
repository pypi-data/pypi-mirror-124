from distutils.core import setup, Extension

setup(
    name='mmhash2',
    version='1.1',
    ext_modules=[
        Extension('mmhash2', ['murmurhash2.h', 'murmurhash2.cpp'], ),
    ],
    description="MurmurHash2 For Python3",
    long_description="""
murmurhash is a fast hash function ::
    >>> import mmhash2

    >>> print(mmhash2.murmurhash64a("zhenhao", 0x1234))
    16299279845682521441

    >>> print(mmhash2.dechex(mmhash2.murmurhash64a("zhenhao", 0x1234)))
    'e232aca990972561'

    >>> print(mmhash2.murmurhash64b('zhenhao', 0x1234))
    4178523214822422458


MurmurHash2 http://murmurhash.googlepages.com/
MurmurHash2, 64-bit versions, by Austin Appleby

Modified by hit_zhenhao@163.com

linux python lib
"""
)
