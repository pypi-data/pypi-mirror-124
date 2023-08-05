import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EasyBlackjack",
    version="0.1.6",
    author="Antonio Granaldi",
    author_email="tonio.granaldi@gmail.com",
    description="A Single-Deck Blackjack hand generator and calculator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antogno/easyblackjack",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)