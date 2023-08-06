from setuptools import setup

name = "types-google-cloud-ndb"
description = "Typing stubs for google-cloud-ndb"
long_description = '''
## Typing stubs for google-cloud-ndb

This is a PEP 561 type stub package for the `google-cloud-ndb` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `google-cloud-ndb`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/google-cloud-ndb. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `3a70f34ddd8a74ded7cafb26b84f27382dd9d798`.
'''.lstrip()

setup(name=name,
      version="1.9.0",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=['types-six'],
      packages=['google-stubs'],
      package_data={'google-stubs': ['__init__.pyi', 'cloud/__init__.pyi', 'cloud/ndb/__init__.pyi', 'cloud/ndb/_batch.pyi', 'cloud/ndb/_cache.pyi', 'cloud/ndb/_datastore_api.pyi', 'cloud/ndb/_datastore_query.pyi', 'cloud/ndb/_eventloop.pyi', 'cloud/ndb/_options.pyi', 'cloud/ndb/_transaction.pyi', 'cloud/ndb/blobstore.pyi', 'cloud/ndb/client.pyi', 'cloud/ndb/context.pyi', 'cloud/ndb/django_middleware.pyi', 'cloud/ndb/exceptions.pyi', 'cloud/ndb/global_cache.pyi', 'cloud/ndb/key.pyi', 'cloud/ndb/metadata.pyi', 'cloud/ndb/model.pyi', 'cloud/ndb/msgprop.pyi', 'cloud/ndb/polymodel.pyi', 'cloud/ndb/query.pyi', 'cloud/ndb/stats.pyi', 'cloud/ndb/tasklets.pyi', 'cloud/ndb/utils.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Typed",
      ]
)
