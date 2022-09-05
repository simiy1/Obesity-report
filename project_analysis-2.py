"""
Name       : Siming Yin, Robert Zheng
UWNetID    : siminy, xzheng23
Description: This file is going to draw the data
             visualization for our project question
             We want to find out the relationship
             between obesity and GDP.
             We also use the GDP and continent to
             develop a machine learning model in order
             to determina the obeisty rate for the country
"""
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import seaborn as sns
import project_main
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier


def categorize_obesity_rate(row):
    """
    Returns the categorization of obesity rate accordingly.
    row - a row in the DataFrame
    """
    val = row['Obesity (%)']
    if val <= 5.0:
        return 'Less than 5%'
    elif val <= 10.0:
        return '5-10%'
    elif val <= 15.0:
        return '10-15%'
    elif val <= 20.0:
        return '15-20%'
    elif val <= 25.0:
        return '20-25%'
    elif val <= 30.0:
        return '25-30%'
    else:
        return 'Above 30%'


def train_gdp_obesity_model(merged):
    """
    Trains a machine learning model to predict/classify the obesity rate
    categorization based on continent and GDP categorization.
    Returns the training accuracy and test accuracy scores.
    merged - the merged DataFrame
    """
    merged_copy = merged.copy()
    gdp_labels = ['Below Q1', 'Q1 - Q2', 'Q2 - Q3', 'Above Q3']
    m_gdp = merged_copy['GDP']
    merged_copy['GDP_category'] = pd.qcut(m_gdp, q=4, labels=gdp_labels)
    merged_copy = merged_copy[merged_copy['Sex'] == 'Both sexes']
    merged_copy['Obesity_category'] = \
        merged_copy.apply(lambda row: categorize_obesity_rate(row), axis=1)
    merged_copy = merged_copy.filter(['continent', 'Obesity_category',
                                      'GDP_category'])

    features = merged_copy.loc[:, merged_copy.columns != 'Obesity_category']
    features = pd.get_dummies(features)
    labels = merged_copy['Obesity_category']
    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.3)

    model = DecisionTreeClassifier()
    model.fit(features_train, labels_train)

    train_predictions = model.predict(features_train)
    train_acc = accuracy_score(labels_train, train_predictions)

    test_predictions = model.predict(features_test)
    test_acc = accuracy_score(labels_test, test_predictions)

    return train_acc, test_acc


def gdp_v_obesity_world(merged):
    """
    Plots a regression plot of GDP vs. obesity rate in the world.
    merged - the merged DataFrame
    """
    fig, ax = plt.subplots(1, figsize=(20, 10))
    sns.regplot(x='GDP', y='Obesity (%)', data=merged, ax=ax)
    ax.set_title('GDP versus Obesity (World)')
    plt.savefig('gdp_v_obesity_world.png')


def gdp_v_obesity_africa(merged):
    """
    Plots a regression plot of GDP vs. obesity rate in Africa.
    merged - the merged DataFrame
    """
    merged_africa = merged[merged['continent'] == 'Africa']
    fig, ax = plt.subplots(1, figsize=(20, 10))
    sns.regplot(x='GDP', y='Obesity (%)', data=merged_africa, ax=ax)
    ax.set_title('GDP versus Obesity (Africa)')
    plt.savefig('gdp_v_obesity_africa.png')


def gdp_v_obesity_asia(merged):
    """
    Plots a regression plot of GDP vs. obesity rate in Asia.
    merged - the merged DataFrame
    """
    merged_asia = merged[merged['continent'] == 'Asia']
    fig, ax = plt.subplots(1, figsize=(20, 10))
    sns.regplot(x='GDP', y='Obesity (%)', data=merged_asia, ax=ax)
    ax.set_title('GDP versus Obesity (Asia)')
    plt.savefig('gdp_v_obesity_asia.png')


def gdp_v_obesity_europe(merged):
    """
    Plots a regression plot of GDP vs. obesity rate in Europe.
    merged - the merged DataFrame
    """
    merged_europe = merged[merged['continent'] == 'Europe']
    fig, ax = plt.subplots(1, figsize=(20, 10))
    sns.regplot(x='GDP', y='Obesity (%)', data=merged_europe, ax=ax)
    ax.set_title('GDP versus Obesity (Europe)')
    plt.savefig('gdp_v_obesity_europe.png')


def gdp_v_obesity_na(merged):
    """
    Plots a regression plot of GDP vs. obesity rate in North America.
    merged - the merged DataFrame
    """
    merged_na = merged[merged['continent'] == 'North America']
    fig, ax = plt.subplots(1, figsize=(20, 10))
    sns.regplot(x='GDP', y='Obesity (%)', data=merged_na, ax=ax)
    ax.set_title('GDP versus Obesity (North America)')
    plt.savefig('gdp_v_obesity_na.png')


def gdp_v_obesity_oceania(merged):
    """
    Plots a regression plot of GDP vs. obesity rate in Oceania.
    merged - the merged DataFrame
    """
    merged_oceania = merged[merged['continent'] == 'Oceania']
    fig, ax = plt.subplots(1, figsize=(20, 10))
    sns.regplot(x='GDP', y='Obesity (%)', data=merged_oceania, ax=ax)
    ax.set_title('GDP versus Obesity (Oceania)')
    plt.savefig('gdp_v_obesity_oceania.png')


def gdp_v_obesity_sa(merged):
    """
    Plots a regression plot of GDP vs. obesity rate in South America.
    merged - the merged DataFrame
    """
    merged_sa = merged[merged['continent'] == 'South America']
    fig, ax = plt.subplots(1, figsize=(20, 10))
    sns.regplot(x='GDP', y='Obesity (%)', data=merged_sa, ax=ax)
    ax.set_title('GDP versus Obesity (South America)')
    plt.savefig('gdp_v_obesity_sa.png')


def main():
    gdp = project_main.clean_gdp('/home/GDP.csv')
    obesity = project_main.clean_obesity('/home/obesity-cleaned.csv')
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    merged = project_main.merge_data(gdp, obesity, world)
    gdp_v_obesity_world(merged)
    gdp_v_obesity_africa(merged)
    gdp_v_obesity_asia(merged)
    gdp_v_obesity_europe(merged)
    gdp_v_obesity_na(merged)
    gdp_v_obesity_oceania(merged)
    gdp_v_obesity_sa(merged)
    train_gdp_obesity_model(merged)


if __name__ == '__main__':
    main()
