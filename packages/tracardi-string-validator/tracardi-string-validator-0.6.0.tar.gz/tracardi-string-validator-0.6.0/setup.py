from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-string-validator',
    version='0.6.0',
    description='The purpose of this plugin is validate data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Patryk Migaj',
    author_email='patromi123@gmail.com',
    packages=['tracardi_string_validator'],
    install_requires=[
        "tracardi-plugin-sdk>=0.6.22",
        "pydantic",
        "tracardi_dot_notation",
        "barcodenumber"
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
