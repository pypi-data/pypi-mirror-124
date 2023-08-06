import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nwmodule", # Replace with your own username
    version="0.3",
    author="Mihai Cristian Pîrvu",
    author_email="mihaicristianpirvu@gmail.com",
    description="Generic PyTorch high level neural API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/neuralwrappers/nwmodule",
    keywords = ["PyTorch", "neural network", "high level api"],
    packages=setuptools.find_packages(),
    install_requires=[],
    license="WTFPL",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
