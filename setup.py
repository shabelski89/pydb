from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydb",
    version="1.3.2",
    author='Aleksandr Shabelsky',
    author_email='a.shabelsky@gmail.com',
    description="Light CLI Oracle, Postgres, Mysql",
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
    python_requires=">=3.6",
    install_requires=[
        "colorama==0.4.4",
        "pep517==0.12.0",
        "wcwidth==0.2.5",
        "zipp==3.6.0",
        "pyparsing==3.0.7",
        "tomli==1.2.3",
        "typing_extensions==4.1.1",
        "importlib-metadata==4.8.3",
        "prettytable==2.5.0",
        "cffi==1.15.1",
        "cryptography==40.0.2",
        "pycparser==2.21",
    ],
    extras_require={
        "oracle": ["cx-Oracle==8.2.1"],
        "postgres": ["psycopg2==2.9.1"],
        "mysql": ["PyMySQL==1.0.2"],
    },
    entry_points={
        'console_scripts': [
            'dbclient = pydb.dbclient:main',
        ]
    },
)
