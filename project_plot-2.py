"""
Name       : Siming Yin, Robert Zheng
UWNetID    : siminy, xzheng23
Description: This file is going to draw the data
             visualization for the top10 and bottom
             10 countries for Obesity rate and GDP.
             We are going to find out those countries
             and point them out on the map.
             We also will plot the trend of GDP and
             obesity rate of those countries over years.
"""
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns
import project_main


def plot_most_obese_10(merged, world):
    """
    Plots a map of 10 countries with highest obesity rate.
    Returns the DataFrame containing them.
    merged - the merged DataFrame
    """
    most_obese = merged[merged['Sex'] == 'Both sexes'] \
        .nlargest(10, 'Obesity (%)')
    fig, ax = plt.subplots(1, figsize=(20, 10))
    world.plot(color='#EEEEEE', ax=ax)
    most_obese.plot(color='#DC143C', legend=True, ax=ax)
    plt.title('The Top 10 Countries with the Highest Obesity Rate')
    plt.savefig('most_obese_10.png')

    return most_obese


def plot_least_obese_10(merged, world):
    """
    Plots a map of 10 countries with lowest obesity rate.
    Returns the DataFrame containing them.
    merged - the merged DataFrame
    """
    least_obese = merged[merged['Sex'] == 'Both sexes'] \
        .nsmallest(10, 'Obesity (%)')
    fig, ax = plt.subplots(1, figsize=(20, 10))
    world.plot(color='#EEEEEE', ax=ax)
    least_obese.plot(color='#0000FF', legend=True, ax=ax)
    plt.title('The bottom 10 Countries with the Lowest Obesity Rate')
    plt.savefig('least_obese_10.png')

    return least_obese


def plot_highest_gdp_10(merged, world):
    """
    Plots a map of 10 countries with highest GDP.
    Returns the DataFrame containing them.
    merged - the merged DataFrame
    """
    highest_gdp = merged[merged['Sex'] == 'Both sexes'].nlargest(10, 'GDP')
    fig, ax = plt.subplots(1, figsize=(20, 10))
    world.plot(color='#EEEEEE', ax=ax)
    highest_gdp.plot(color='#DC143C', legend=True, ax=ax)
    plt.title('The Top 10 Countries with the Highest GDP')
    plt.savefig('highest_gdp_10.png')

    return highest_gdp


def plot_lowest_gdp_10(merged, world):
    """
    Plots a map of 10 countries with lowest GDP.
    Returns the DataFrame containing them.
    merged - the merged DataFrame
    """
    lowest_gdp = merged[merged['Sex'] == 'Both sexes'].nsmallest(10, 'GDP')
    fig, ax = plt.subplots(1, figsize=(20, 10))
    world.plot(color='#EEEEEE', ax=ax)
    lowest_gdp.plot(color='#0000FF', legend=True, ax=ax)
    plt.title('The Bottom 10 Countries with the Lowest GDP')
    plt.savefig('lowest_gdp_10.png')

    return lowest_gdp


def plot_gdp_trend(gdp, highest_gdp, lowest_gdp):
    """
    Plots the trend of gdp over years of 10 countries with highest/lowest GDP
    gdp - the DataFrame containing the GDP of countries
    highest_gdp - the DataFrame containing 10 countries with the highest GDP
    lowest_gdp - the DataFrame containing 10 countries with the lowest GDP
    """
    gdp_top = highest_gdp.merge(gdp, left_on='Country Code',
                                right_on='Country Code', how='left')
    gdp_bottom = lowest_gdp.merge(gdp, left_on='Country Code',
                                  right_on='Country Code', how='left')
    gdp_top = gdp_top.filter(['Country', 'GDP_y', 'Year_y'])
    gdp_bottom = gdp_bottom.filter(['Country', 'GDP_y', 'Year_y'])
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(20, 10))
    sns.lineplot(x='Year_y', y='GDP_y', data=gdp_top, hue='Country', ax=ax1)
    ax1.set_title('The trend of the GDP over years (Top 10 countries in 2016)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('GDP')
    sns.lineplot(x='Year_y', y='GDP_y', data=gdp_bottom, hue='Country', ax=ax2)
    ax2.set_title('The trend of GDP over years (Bottom 10 countries in 2016)')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('GDP')
    plt.savefig('gdp_trend.png')


def plot_obesity_trend(obesity, most_obese, least_obese):
    """
    Plots the trend of gdp over years of 10 countries with highest/lowest
    obesity rate.
    obesity - the DataFrame containing the obesity rate of countries
    highest_gdp - the DataFrame containing 10 countries with the highest
    obesity rate.
    lowest_gdp - the DataFrame containing 10 countries with the lowest
    obesity rate.
    """
    obesity_filter = obesity[obesity['Sex'] == 'Both sexes']
    obesity_top = most_obese.merge(obesity_filter, left_on='Country',
                                   right_on='Country', how='left')
    obesity_bottom = least_obese.merge(obesity_filter, left_on='Country',
                                       right_on='Country', how='left')
    obesity_top = obesity_top.filter(['Country', 'Obesity (%)_y', 'Year_y'])
    obesity_bottom = obesity_bottom.filter(['Country',
                                            'Obesity (%)_y', 'Year_y'])
    fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(20, 10))
    sns.lineplot(x='Year_y', y='Obesity (%)_y',
                 data=obesity_top, hue='Country', ax=ax1)
    ax1.set_title('The trend of obesity rate (Top 10 countries in 2016)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Obesity rate')
    sns.lineplot(x='Year_y', y='Obesity (%)_y',
                 data=obesity_bottom, hue='Country', ax=ax2)
    ax2.set_title('The trend of obesity rate (Bottom 10 countries in 2016)')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Obesity rate')
    plt.savefig('obesity_trend.png')


def main():
    gdp = project_main.clean_gdp('/home/GDP.csv')
    obesity = project_main.clean_obesity('/home/obesity-cleaned.csv')
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    merged = project_main.merge_data(gdp, obesity, world)
    most_obese = plot_most_obese_10(merged, world)
    least_obese = plot_least_obese_10(merged, world)
    highest_gdp = plot_highest_gdp_10(merged, world)
    lowest_gdp = plot_lowest_gdp_10(merged, world)
    plot_gdp_trend(gdp, highest_gdp, lowest_gdp)
    plot_obesity_trend(obesity, most_obese, least_obese)


if __name__ == '__main__':
    main()
