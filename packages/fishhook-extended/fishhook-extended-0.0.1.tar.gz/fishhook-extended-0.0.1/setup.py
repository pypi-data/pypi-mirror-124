import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fishhook-extended",
    version="0.0.1",
    author="Crowthebird",
    author_email="nohackingofkrowten@gmail.com",
    description="Extended: Allows for runtime hooking of static class functions AND other type slots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thatbirdguythatuknownot/fishhook-extended",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
