import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="popcat_wrapper",
    version="1.3",
    author="NotFaizen",
    author_email="munavir370@gmail.com",
    url = "https://github.com/NotFaizen/popcat_wrapper",
    description="A wrapper designed for easy image manipulation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=['python', 'async', 'popcat', 'popcatapi', 'api', 'api wrapper','discord','wrapper'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["aiohttp"]
)