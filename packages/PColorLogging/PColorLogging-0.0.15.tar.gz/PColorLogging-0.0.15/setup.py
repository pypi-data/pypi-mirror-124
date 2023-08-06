import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PColorLogging",
    version="0.0.15",
    author="Phạm Hồng Phúc",
    author_email="phamhongphuc12atm1@gmail.com",
    description="This is powerful logging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phamhongphuc1999/PColorLog",
    project_urls={
        "Bug Tracker": "https://github.com/phamhongphuc1999/PColorLog",
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