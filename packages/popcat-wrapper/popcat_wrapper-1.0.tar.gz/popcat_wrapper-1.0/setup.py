import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="popcat_wrapper",
    version="1.0",
    author="NotFaizen",
    author_email="munavir370@gmail.com",
    url = "https://github.com/NotFaizen/popcat_wrapper",
    description="A wrapper designed for easy image manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "popcat"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["aiohttp"]
)