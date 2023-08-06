from setuptools import setup

setup(
    name='abstract builder',  # package name
    version='1.0',  # version
    author='FullDUngeon',
    author_email='ddd.dungeon@gmail.com',
    description='Преобразование конспектов в HTML-документы',  # short description
    long_description="readme.md",
    long_description_content_type="text/markdown",
    url="https://github.com/FullDungeon/abstract_builder",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',

    install_requires=['importlib_resources'],  # list of packages this package depends on.

    packages=['abstract_builder'],  # List of module names that installing this package will provide.
    package_data={
        'abstract_builder': ['static/style.css', 'static/main.js']
    },

    entry_points={
        'console_scripts': [
            'abstract-builder = abstract_builder.cmd:build_command',
        ],
    },
)
