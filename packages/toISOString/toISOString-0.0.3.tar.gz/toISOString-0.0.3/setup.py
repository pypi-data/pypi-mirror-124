import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="toISOString",
    version="0.0.3",
    author="Kaleo Cheng",
    entry_points={},
    author_email="kaleocheng@gmail.com",
    description="",
    long_description=long_description,
    package_data={},
    long_description_content_type="text/markdown",
    url="https://github.com/kaleocheng/toISOString",
    install_requires=[],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
