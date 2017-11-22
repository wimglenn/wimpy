from setuptools import find_packages, setup

setup(
    name='wimpy',
    version='0.2',
    description='Anti-copy-pasta',
    url='https://github.com/wimglenn/wimpy',
    author='Wim Glenn',
    author_email='hey@wimglenn.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
)
