from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pydb",
    version="1.0.1",
    author='Aleksandr Shabelsky',
    author_email='a.shabelsky@gmail.com',
    description="Oracle, Postgres, Mysql in one package",
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
    install_requires=['PyMySQL', 'psycopg2', 'cx_Oracle'],
)
