from setuptools import setup

setup(
    name="wimpy",
    version="0.6",
    description="Anti-copy-pasta",
    long_description=open('README.rst').read(),
    url="https://github.com/wimglenn/wimpy",
    author="Wim Glenn",
    author_email="hey@wimglenn.com",
    license="MIT",
    packages=["wimpy"],
    options={"bdist_wheel": {"universal": True}},
)
