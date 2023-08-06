# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name="datara",
    version="0.0.0-dev",
    author="Datarock technologies",
    author_email='datara@datarock.tech',
    description="auto tester for your AI",
    url="https://github.com/datarocktech/datara",
    project_urls={
        "Bug Tracker": "https://github.com/datarocktech/datara/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=('examples')),
    python_requires=">=3.6",
    install_requires=[
        'pandas',
        'termcolor',
        'dill'
    ],
)
