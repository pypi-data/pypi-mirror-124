from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

# tests_require = ["vcrpy>=1.10.3",]

setup(
    name="monkeytools",
    version="0.4",
    description="A personal collection of algorithms and tools for the standard code monkey.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Matthew DeVerna",
    author_email="mdeverna@iu.edu",
    url="https://github.com/mr-devs/monkeytools",
    project_urls={
        "Documentation": "https://github.com/mr-devs/monkeytools",
        "Issue Tracker": "https://github.com/mr-devs/monkeytools/issues",
        "Source Code": "https://github.com/mr-devs/monkeytools",
    },
    download_url="https://github.com/mr-devs/monkeytools",
    packages=["monkeytools"],
    # install_requires=[],
    # tests_require=tests_require,
    python_requires=">=3.5",
)