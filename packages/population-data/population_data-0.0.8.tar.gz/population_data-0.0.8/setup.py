from setuptools import setup, find_packages
import pathlib

# this directory
here = pathlib.Path(__file__).parent

long_description = (here / "README.md").read_text()


VERSION = '0.0.8'
DESCRIPTION = 'Get Population Data of the world'

# Setting up
setup(
    name="population_data",
    version=VERSION,
    author="Anshu (Pydjango and techitutorials.com)",
    author_email="<anshupal258@gmail.com>",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://techitutorial.com",
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'population', 'data',
              'api', 'worldometer', 'population_data']
)
