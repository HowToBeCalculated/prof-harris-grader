from setuptools import setup, find_packages

setup(
    name='prof_harris_grader',
    version='0.1.0',
    description='Grader for Professor Harris MKT 461 class',
    author='Professor Harris',
    packages=find_packages(),
    install_requires=[
        'dill',
        'requests',
    ],
)