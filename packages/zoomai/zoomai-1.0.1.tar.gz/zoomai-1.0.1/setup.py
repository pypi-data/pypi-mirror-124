
from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="zoomai",
    version="1.0.1",
    description="A Python package to get the world.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mandiladitya",
    author="Aditya Mandil",
    author_email="adityamandil317@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["hello_pypi"], # the name of outer folder
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "hello-pypi=hello_pypi.cli:main", # entry point 
        ]
    },
)
