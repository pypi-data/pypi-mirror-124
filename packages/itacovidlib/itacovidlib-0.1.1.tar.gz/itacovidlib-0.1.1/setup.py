from setuptools import find_packages, setup
import os

def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='itacovidlib',
    packages=find_packages(),
    version='0.1.1',
    description='Python library for COVID-19 infections and vaccinations in Italy data retrieval and analysis',
    author='Federico Corchia',
    license='MIT',
    keywords='COVID-19 infection vaccination Italy',
    url='https://github.com/FedericoCorchia/Italian_COVID_Library',
    download_url='https://github.com/FedericoCorchia/itacovidlib/archive/refs/tags/v0.1.1-alpha.tar.gz',
    long_description=read('README.md'),
    install_requires=['numpy', 'pandas', 'geopandas', 'requests', 'epyestim'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        ],
)
