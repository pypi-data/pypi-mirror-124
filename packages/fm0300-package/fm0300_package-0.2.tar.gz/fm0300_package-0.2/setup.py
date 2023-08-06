from setuptools import setup


setup(
    name='fm0300_package',                    # package name
    version='0.2',                          # version
    description='Package Description',      # short description
    author='Stephen Hudson',
    author_email='shudson@anl.gov',
    url='http://example.com',               # package URL
    install_requires=['numpy>1.17.0'],                    # list of packages this package depends
                                            # on.
    packages=['fm0300_package'],              # List of module names that installing
                                            # this package will provide.
) 