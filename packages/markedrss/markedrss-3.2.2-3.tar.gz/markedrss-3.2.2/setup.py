import os

from setuptools import find_packages, setup


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as file:
        return file.read()


setup(
    name="markedrss",
    version="3.2.2",
    author="doppelmarker",
    author_email="doppelmarker@gmail.com",
    url="https://github.com/doppelmarker/Homework",
    description="Pure Python command-line RSS reader",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "pydantic",
        "Jinja2",
        "xhtml2pdf",
        "ebooklib",
        "colorama",
    ],
    extras_require={
        "aiohttp": ["aiohttp"],
    },
    entry_points={
        "console_scripts": ["markedrss=rss_reader.__main__:main"],
    },
)
