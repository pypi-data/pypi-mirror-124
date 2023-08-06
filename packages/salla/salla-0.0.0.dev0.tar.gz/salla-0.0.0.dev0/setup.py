from setuptools import setup, find_packages

KEYWORD = [
    "salla",
    "salla api",
]

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()


setup(
    name="salla",
    version="0.0.0.dev0",
    description="Python Salla api.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TheAwiteb",
    author_email="Awiteb@hotmail.com",
    url="https://github.com/TheAwiteb/salla",
    packages=find_packages(),
    license="MIT",
    keywords=KEYWORD,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
