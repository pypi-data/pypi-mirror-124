import setuptools
import pathlib
from setuptools import setup

path = pathlib.Path(__file__).resolve().parent
read_desc = (path / "README.md").read_text()

setup(
    name="PyViO",
    version="1.2.0",
    description="Visualize outliers in data",
    long_description=read_desc,
    long_description_content_type="text/markdown",
    author="Team_PyViO",
    author_email = 'team.pyvio@gmail.com',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
    ],
    packages=setuptools.find_packages(exclude=['test']),
    include_package_data=True,
    install_requires=['numpy','pandas','plotly','matplotlib','cufflinks','wikipedia']
)
