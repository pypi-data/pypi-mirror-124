import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Line automatically modified by acpoa-builder
# Do not modify it manually unless you know what you are doing
files = []

setuptools.setup(
    name="____name____",
    version="____version____",
    author="____author____",
    author_email="____author_email____",
    description="____description____",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="____url____",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    package_data={'': files}
)
