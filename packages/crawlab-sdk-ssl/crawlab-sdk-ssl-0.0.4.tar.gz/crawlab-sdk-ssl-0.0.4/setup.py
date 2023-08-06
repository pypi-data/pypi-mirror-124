from setuptools import setup, find_packages

import crawlab.config


setup(
    name="crawlab-sdk-ssl",
    version="0.0.4",
    packages=find_packages(),
    url="https://github.com/crawlab-team/crawlab-sdk",
    license="BSD-3-Clause",
    author="tikazyq",
    author_email="tikazyq@163.com",
    description="Python SDK for Crawlab",
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "click==7.0",
        "requests==2.22.0",
        "prettytable==0.7.2",
        "scrapy==2.5.0",
        "pymongo==3.10.1",
        "pymysql==0.9.3",
        "psycopg2-binary==2.8.5",
        "kafka-python==2.0.1",
        "elasticsearch==7.8.0",
        "pathspec==0.8.0",
    ],
    entry_points={"console_scripts": ["crawlab=crawlab:main"]},
)
