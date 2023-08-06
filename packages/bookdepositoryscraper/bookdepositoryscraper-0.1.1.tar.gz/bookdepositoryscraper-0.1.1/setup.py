from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="bookdepositoryscraper",
    version="0.1.1",
    description="Scraper for the Book Depository website",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/adeyinkaoresanya/bookdepositoryscraper",
    author="AdeyinkaOresanya",
    author_email="adeyinkaoresanya@gmail.com",
    keywords="core package",
    license="MIT",
    py_modules = ["scraper", "preprocess"],
    packages= find_packages('src'), 
    package_dir= {"": "src"},
    python_requires= ">=3.6"
    )