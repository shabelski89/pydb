from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydb",
    version="1.2.4",
    author='Aleksandr Shabelsky',
    author_email='a.shabelsky@gmail.com',
    description="Light console client for Oracle, Postgres, Mysql",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://gitlab.seventest/sa/pydb",
    project_urls={
        "Bug Tracker": "http://gitlab.seventest/sa/pydb/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=[
        "colorama==0.4.4",
        "cx-Oracle==8.2.1",
        "pep517==0.12.0",
        "psycopg2==2.9.1",
        "PyMySQL==1.0.2",
        "pyparsing==3.0.7",
        "tomli==2.0.1",
        "prettytable==3.5.0",
    ],
    entry_points={
        'console_scripts': [
            'dbclient = pydb.dbclient:main',
        ]
    },
)
