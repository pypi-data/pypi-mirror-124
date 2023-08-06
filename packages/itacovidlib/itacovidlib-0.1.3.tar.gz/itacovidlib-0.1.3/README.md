# Italian COVID Library (itacovidlib)
![Italian COVID Library logo](https://github.com/FedericoCorchia/Italian_COVID_Library/blob/main/logo.png)

A Python library for COVID-19 infections and vaccinations in Italy data retrieval and analysis.

## Installing Italian COVID Library
You can install this library directly from PyPi:

`pip install itacovidlib`

You can also just clone this repository and use it as a normal Python package:

`git clone https://github.com/FedericoCorchia/itacovidlib`

## Requirements
Functioning of Italian COVID Library requires the following:
- Python (3.8.1 or higher)
- numpy
- pandas (1.2.0 or higher)
- geopandas (0.7.0 or higher)
- requests
- epyestim
- setuptools

## Usage
Instructions on using Italian COVID Library, also including practical examples:

[Italian COVID Library Tutorial](https://github.com/FedericoCorchia/Italian_COVID_Library/blob/main/Tutorial.ipynb)

## Data Sources
For data on COVID-19 cases in Italy: [pcm-dpc/COVID-19](https://github.com/pcm-dpc/COVID-19) - "COVID-19 Italia - Monitoraggio situazione" by Dipartimento della Protezione Civile

For data on vaccinations in Italy: [italia/covid19-opendata-vaccini](https://github.com/italia/covid19-opendata-vaccini) - "Open Data su consegna e somministrazione dei vaccini anti COVID-19 in Italia - Commissario straordinario per l'emergenza Covid-19", by Commissario straordinario per l'emergenza Covid-19 - Presidenza del Consiglio dei Ministri

Both are released under **Creative Commons - Attribution 4.0 International (CC BY 4.0)** [Full license](https://creativecommons.org/licenses/by/4.0/legalcode) - [Summary](https://creativecommons.org/licenses/by/4.0/deed.en)

For .geojson files with Italian regions and provinces: [datajournalism-it/regioni-con-trento-bolzano.geojson](https://gist.github.com/datajournalism-it/f1abb68e718b54f6a0fe) and [datajournalism-it/province.geojson](https://gist.github.com/datajournalism-it/212e7134625fbee6f9f7) by Datajournalism.it

Downloader functions provide the original data as they are without any modification apart from translating them into English and optimising their presentation.

## Further project details
This is a programming project for the Software and Computing for Nuclear and Subnuclear Physics course, Master Course in Nuclear and Subnuclear Physics, University of Bologna.
