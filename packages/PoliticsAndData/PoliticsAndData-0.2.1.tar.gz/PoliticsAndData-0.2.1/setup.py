from setuptools import setup


setup(
    name="PoliticsAndData",
    version="0.2.1",
    description="Easily summarize the csv data files from https://politicsandwar.com/data/",
    url="https://github.com/pythonian23/PoliticsAndData",
    author="pythonian23",
    license="MPL-2.0",
    install_requires=[
        'requests >= 2.0.0',
        'pytz >= 2020.0',
        'regex >= 2020.0.0'
    ],
    packages=["pnd"]
)
