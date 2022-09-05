"""
Name       : Siming Yin, Robert Zheng
UWNetID    : siminy, xzheng23
Description: This file is going to read the dataset
             and clean or refine our dataset.
             We also merge the dataset so that it
             will be usable for our project analysis
"""
import pandas as pd


def clean_obesity(file_name):
    """
    This function is going to take the obesity dataset as a parameter
    and refine and fix the value in the dataset. So that the dataset
    will be usable in our further study
    """
    obesity = pd.read_csv(file_name, na_values='No data')
    obesity["Obesity (%)"] = obesity["Obesity (%)"] \
        .str.replace(r"(\s*\[.*?\]\s*)", "", regex=True) \
        .str.strip().str.slice(0, 3)
    obesity = obesity.astype({'Obesity (%)': 'float64'})
    return obesity


def clean_gdp(file_name):
    """
    This function is going to take the gdp dataset as a parameter
    and refine and fix the value  type in the dataset.
    We also are going to change the dataset structure,
    make the wide dataset structure into long dataset structure
    So that the dataset will be usable in our further study
    """
    gdp = pd.read_csv(file_name)
    gdp = gdp.reset_index()
    gdp = pd.melt(gdp, id_vars='Country Code',
                  value_vars=["1990", "1991", "1992", "1993", "1994", "1995",
                              "1996", "1997", "1998", "1999", "2000", "2001",
                              "2002", "2003", "2004", "2005", "2006", "2007",
                              "2008", "2009", "2010", "2011", "2012", "2013",
                              "2014", "2015", "2016", "2017", "2018", "2019"])
    gdp = gdp.rename(columns={"variable": "Year", "value": "GDP"})
    gdp = gdp.astype({'Year': 'int'})
    return gdp


def merge_data(gdp, obesity, world):
    """
    In this function, we takes gdp and obesity these two data as parameter,
    we are going to merge these two data together. Since we are going to
    use the most recent year for the data analysis. It will filter by 2016,
    which it most recent year in both dataset.
    Since the country name are different in both dataset, we use the third
    dataset 'countries' to help connect those two dataset together.
    Lastly, we use the 'world' dataset(parameter)
    in order to make the map visualization
    """
    countries = pd.read_excel('/home/country_codes.xlsx')
    obesity_m = obesity[(obesity['Year'] == 2016)].dropna()
    gdp_m = gdp.loc[gdp['Year'] == 2016]
    merged = obesity_m.merge(countries, left_on='Country',
                             right_on='Short name')
    merged = merged.filter(['Country', 'Obesity (%)', 'Sex', 'ISO3'])
    merged = merged.merge(gdp_m, left_on='ISO3', right_on='Country Code')
    merged = world.merge(merged, left_on='iso_a3', right_on='ISO3')
    merged = merged.dropna()
    return merged
