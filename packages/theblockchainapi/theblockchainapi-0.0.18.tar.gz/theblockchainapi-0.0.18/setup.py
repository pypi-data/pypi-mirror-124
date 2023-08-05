import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="theblockchainapi",
    version="0.0.18",
    author="BlockX",
    author_email="info@theblockchainapi.com",
    description="Blockchain made easy. Find out more at docs.theblockchainapi.com.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BL0CK-X/the-blockchain-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)
