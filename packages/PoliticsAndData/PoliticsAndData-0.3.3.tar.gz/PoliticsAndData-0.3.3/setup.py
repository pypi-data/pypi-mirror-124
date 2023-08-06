from setuptools import setup


setup(
    name="PoliticsAndData",
    version="0.3.3",
    description="Easily summarize the csv data files from https://politicsandwar.com/data/",
    url="https://github.com/pythonian23/PoliticsAndData",
    author="pythonian23",
    license="MPL-2.0",
    requires=[
        "requests",
        "pytz",
        "regex"
    ],
    packages=["pnd"]
)
