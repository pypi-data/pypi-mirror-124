import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyelves",
    version="0.0.1",
    author="Alex Pylypenko",
    author_email="macaquedev@gmail.com",
    description="A package designed to make Python programming easier.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["elves"],
    python_requires=">=3.6",
)