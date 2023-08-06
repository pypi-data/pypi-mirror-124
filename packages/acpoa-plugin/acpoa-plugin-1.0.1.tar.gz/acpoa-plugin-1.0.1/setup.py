import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acpoa-plugin",
    version="1.0.1",
    author="Leikt",
    author_email="leikt.solreihin@gmail.com",
    description="ACPOA plugin creation helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Leikt/acpoa-plugin",
    project_urls={
        "Bug Tracker": "https://github.com/Leikt/acpoa-plugin/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    package_data={'acpoa-plugin': ['default/*', 'default/src/plugin_name/*']},
    install_requires=['build']
)
