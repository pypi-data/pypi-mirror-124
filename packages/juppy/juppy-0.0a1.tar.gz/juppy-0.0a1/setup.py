import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="juppy",
    version="0.0.a1",
    author="Hamstory Studio",
    author_email="hamstory.game.studio@gmail.com",
    description="Simple Databases and Storage for projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexbronikitin/juppy",
    project_urls={
        "Bug Tracker": "https://github.com/alexbronikitin/juppy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)