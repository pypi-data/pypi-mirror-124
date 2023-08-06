from setuptools import setup

setup(
    name='abstract builder',                   # package name
    version='0.20',                            # version
    description='Not working',                 # short description
    install_requires=['importlib_resources'],  # list of packages this package depends on.

    packages=['abstract_builder'],             # List of module names that installing this package will provide.
    package_data={
        'abstract_builder': ['static/style.css', 'static/main.js']
    },

    entry_points={
        'console_scripts': [
            'abstract-builder = abstract_builder.cmd:build_command',
        ],
    },
)
