from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with open('README.md', 'w+') as readme_file:
    readme_file.read()

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


# Setting up
setup(
    name="printful",
    version="1.0.0",
    author="yuma061",
    author_email="",
    description="print() but for nerds.",
    long_description_content_type="text/markdown",
    long_description="If you use print() alot and feel like you want to spice it up a litle then this package is the best choice.",
    packages=find_packages(),
    install_requires=["colorama"],
    keywords=["python", "print"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)