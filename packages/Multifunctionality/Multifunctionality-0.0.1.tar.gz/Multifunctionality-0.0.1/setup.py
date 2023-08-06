import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Multifunctionality",
    version="0.0.1",
    author="Vihaan Mathur & Harihar Rengan",
    author_email="vihaan.harihar341@gmail.com",
    description="The number one package for utilities from a trustworthy source",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages = ["Multifunctionality"],
    python_requires=">=3.6",
    install_requires=["keyboard", "mouse", "playsound==1.2.2"],
)
