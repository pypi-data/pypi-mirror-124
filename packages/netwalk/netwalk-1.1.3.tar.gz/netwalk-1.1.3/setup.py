# -*- coding: UTF-8 -*-
import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "netwalk",
    version = "1.1.3",
    author = "Federico Tabbò (Europe)",
    author_email = "federico.tabbo@global.ntt",
    description = "Network discovery and analysis tool",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://scm.dimensiondata.com/italy/netwalk",
    project_urls = {
        "Bug Tracker": "https://scm.dimensiondata.com/italy/netwalk/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages = setuptools.find_packages(),
    python_requires = ">=3.6",
    install_requires=[
        "ciscoconfparse==1.5.30",
        "napalm==3.2.0"
    ],
    include_package_data=True
)