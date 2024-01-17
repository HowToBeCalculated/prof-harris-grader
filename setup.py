from setuptools import setup, find_packages

setup(
    name='prof-harris-grader',
    version='0.0.1',
    description='Grader for Professor Harris MKT 461 class',
    author='Professor Harris',
    packages=find_packages(),
    install_requires=[
        'dill',
        'requests',
    ],
)