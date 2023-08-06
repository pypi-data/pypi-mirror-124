import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scripting_tools",
    version="0.1.0",
    author="Terroid#0490",
    author_email="skandabhairava@gmail.com",
    description="Scripting toolbox for developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skandabhairava/Scripting_tools",
    project_urls={
        "Bug Tracker": "https://github.com/skandabhairava/Scripting_tools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9"
)