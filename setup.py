"""Installer for the redturtle.tiles.management package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
    + "\n"
)


setup(
    name="redturtle.tiles.management",
    version="4.0.0",
    description="An alternative method for handling and showing tiles",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone",
    author="RedTurtle Technology",
    author_email="sviluppoplone@redturtle.it",
    url="http://pypi.python.org/pypi/redturtle.tiles.management",
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["redturtle", "redturtle.tiles"],
    package_dir={"": "src"},
    python_requires=">=3.11",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "plone.api",
        "plone.app.blocks>=4.0.0",
        "plone.app.tiles",
        "setuptools",
        "z3c.jbot",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            "plone.testing>=5.0.0",
            "plone.app.contenttypes[test]",
            "plone.restapi[test]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
