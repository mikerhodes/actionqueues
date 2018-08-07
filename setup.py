from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='actionqueues',
    version='0.8.2',
    description='Framework for executing actions and rollbacks',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/mikerhodes/actionqueues',
    author='Mike Rhodes',
    author_email='mike.rhodes@dx13.co.uk',
    license='Apache 2.0',
    packages=['actionqueues'],
    zip_safe=False,
    classifiers=(
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
)
