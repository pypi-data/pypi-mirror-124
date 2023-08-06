from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hellow_World",
    version="0.0.1",
    description="A package to difficult task of printing 'Hello World'.",
    author='Mohammad S.Niaei',
    author_email='m.shemuni@gmail.com',
    url='https://github.com/mshemuni/hellow_world',
    py_modules=['__init__'],
    packages=find_packages(exclude=["example.ipynb"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ]

)
