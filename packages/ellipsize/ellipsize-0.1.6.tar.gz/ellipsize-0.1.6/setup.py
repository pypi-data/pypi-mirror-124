import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

from src.ellipsize import version

setuptools.setup(
    name="ellipsize",
    version=version.VERSION,
    author="Andrey Sorokin",
    author_email="andrey@sorokin.engineer",
    description="Pretty reducing huge Python objects to visualise them nicely.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://andgineer.github.io/ellipsize/",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=requirements,
    python_requires=">=3.7",
    keywords="ellipsis log print",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
