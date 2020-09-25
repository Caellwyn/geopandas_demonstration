# -*- coding: utf-8 -*-


import geopandas
import pandas as pd
from zipfile import ZipFile

def get_data()
    zipdata = ZipFile('WDI_csv.zip')
    zipdata.extract('WDIData.csv')
    indicators = pd.read_csv(zipdata.open('WDIData.csv'))
    zipdata.close()
    earth = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

    indicators = indicators[indicators['Indicator Name'] == 
                        'Total greenhouse gas emissions (kt of CO2 equivalent)']
    emdf = indicators.loc[:,['Country Name','Country Code','2012']]
    emdf.set_index('Country Code',inplace = True)
    earth.set_index('iso_a3',inplace = True)
    df = emdf.join(earth, how = 'inner').drop(columns = ['name'])
    df = geopandas.GeoDataFrame(df)
    df.rename(columns = {'2012':'2012 Total Emissions in 1000s of Kilotons of Equivalent C02',
                        'pop_est':'Estimated Population in 1000s',
                        'gdp_md_est':'Estimated GDP in 1000s of US Dollars',
                        'continent':'Continent'},
            inplace = True)
    df['Estimated Population in 1000s'] = df['Estimated Population in 1000s']/1000
    df['Kiloton C02 Eqivalent Emissions per Person'] = df['2012 Total Emissions in 1000s of Kilotons of Equivalent C02']/df['Estimated Population in 1000s']
    geo = df['geometry']
    df.drop(columns = ['geometry'],inplace = True)
    df.insert(len(df.columns),'geometry',geo)

    df.to_csv('/content/emissions_geodata.csv', index = False)