import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qqlog",
    version="0.0.5",
    author="Sheauren Wang",
    author_email="sheauren@gmail.com",
    description="quick method log/exception catching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sheauren/qqlog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)