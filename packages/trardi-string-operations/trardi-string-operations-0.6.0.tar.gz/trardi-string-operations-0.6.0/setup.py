from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='trardi-string-operations',
    version='0.6.0',
    description='This plug-in is to make a string operations like: lowercase remove spaces split and other',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Patryk Migaj',
    packages=['tracardi_string_operations'],
    install_requires=[
        'tracardi-plugin-sdk>=0.6.22'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)