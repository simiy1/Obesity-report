"""
Name       : Siming Yin, Robert Zheng
UWNetID    : siminy, xzheng23
Description: This file is going to test our result in
             the project_analysis.py and project_main.py
"""
import pandas as pd
import project_main
import project_analysis
from cse163_utils import assert_equals
import geopandas as gpd


def test_obesity_data(file_name):
    """
    This function is going to test the obesity data set
    to see if we actually remove the [] and change the type
    value of in "Obesity (%)" column from object to float
    """
    obesity = project_main.clean_obesity(file_name)
    assert_equals(0.1, obesity["Obesity (%)"][0])
    assert_equals(3.6, obesity["Obesity (%)"][5])
    assert_equals(0.4, obesity["Obesity (%)"][15])
    assert_equals(6.8, obesity["Obesity (%)"][38])


def test_gdp_data(file_name):
    """
    This function is going to test the gdp dataset
    to see if we actually reshape the dataset from wide
    to long dataset.
    """
    gdp = pd.read_csv(file_name)
    print('Before change: \n', gdp.head(3))
    gdp = project_main.clean_gdp(file_name)
    print('After change: \n', gdp.head(3))


def test_merged(gdp, obesity, world):
    """
    This function is going to test our merged dataframe
    it will print out the column name before and after
    the merging in order to make sure
    that we have merged two dataset successfully
    """
    print("Before merge:")
    print("gdp data: \n", list(gdp.columns))
    print("obesity data: \n", list(obesity.columns))
    merged = project_main.merge_data(gdp, obesity, world)
    print("After merge:")
    print(list(merged.columns))
    return merged


def test_categorize_obesity_rate():
    """
    Tests the output of categorize_obesity_rate in project_analysis.py.
    """
    data = [['a', 4.9], ['b', 9.9], ['c', 14.9], ['d', 19.9],
            ['e', 24.9], ['f', 29.9], ['g', 30.1], ['h', 99],
            ['i', 0]]
    df = pd.DataFrame(data, columns=['Letter', 'Obesity (%)'])
    result = list()
    for i in range(9):
        result.append(project_analysis.categorize_obesity_rate(df.iloc[i]))
    assert_equals('Less than 5%', result[0])
    assert_equals('5-10%', result[1])
    assert_equals('10-15%', result[2])
    assert_equals('15-20%', result[3])
    assert_equals('20-25%', result[4])
    assert_equals('25-30%', result[5])
    assert_equals('Above 30%', result[6])
    assert_equals('Above 30%', result[7])
    assert_equals('Less than 5%', result[8])


def test_train_gdp_obesity_model(merged):
    """
    Prints the output of train_gdp_obesity_model in project_analysis.py
    and the correlation coefficient of the merged dataset. If the difference
    between the values is reasonably small, we consider our model accurate.
    """
    train_acc, test_acc = project_analysis.train_gdp_obesity_model(merged)
    corr_coef = merged.corr(method='pearson')['Obesity (%)']['GDP']
    print('The correlation coefficient is: ' + str(corr_coef))
    print('The train set accuracy is     : ' + str(train_acc))
    print('The test set accuracy is      : ' + str(test_acc))


def test_plot_most_obese_10(merged, world):
    """
    This function takes merged and world this two dataset
    to test if we find the correct top 10 countries with
    the highest obesity rate. We are using a small dataset
    We print out the dataset with sorted obesity rate in the
    main, and we print out the result in this function.
    By compare those dataset, we make sure we find the correct
    top 10 countries.
    """
    result = project_analysis.plot_most_obese_10(merged, world)
    result = result.filter(['Country', 'Obesity (%)'])
    print(result)


def test_plot_least_obese_10(merged, world):
    """
    This function takes merged and world this two dataset
    to test if we find the correct bottom 10 countries with
    the lowest obesity rate. We are using a small dataset
    We print out the dataset with sorted obesity rate in the
    main, and we print out the result in this function.
    By compare those dataset, we make sure we find the correct
    bottom 10 countries.
    """
    result = project_analysis.plot_least_obese_10(merged, world)
    result = result.filter(['Country', 'Obesity (%)'])
    print(result)


def test_plot_highest_gdp_10(merged, world):
    """
    This function takes merged and world this two dataset
    to test if we find the correct top 10 countries with
    the highest gdp. We are using a small dataset
    We print out the dataset with sorted gdp in the
    main, and we print out the result in this function.
    By compare those dataset, we make sure we find the correct
    top 10 countries.
    """
    result = project_analysis.plot_highest_gdp_10(merged, world)
    result = result.filter(['Country', 'GDP'])
    print(result)


def test_plot_lowest_gdp_10(merged, world):
    """
    This function takes merged and world this two dataset
    to test if we find the correct bottom 10 countries with
    the lowest gdp. We are using a small dataset
    We print out the dataset with sorted gdp in the
    main, and we print out the result in this function.
    By compare those dataset, we make sure we find the correct
    bottom 10 countries.
    """
    result = project_analysis.plot_lowest_gdp_10(merged, world)
    result = result.filter(['Country', 'GDP'])
    print(result)


def main():
    gdp_file = '/home/GDP.csv'
    obesity_file = '/home/test_obesity data.csv'
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    test_obesity_data(obesity_file)
    test_gdp_data(gdp_file)
    merged = test_merged(project_main.clean_gdp(gdp_file),
                         project_main.clean_obesity(obesity_file), world)
    merged_obesity_sort = merged.sort_values(by=['Obesity (%)'])
    merged_obesity_sort = merged_obesity_sort.filter(['Country',
                                                      'Obesity (%)'])
    print(merged_obesity_sort)
    test_plot_most_obese_10(merged, world)
    test_plot_least_obese_10(merged, world)
    merged_gdp_sort = merged.sort_values(by=['GDP'])
    merged_gdp_sort = merged_obesity_sort.filter(['Country',
                                                  'GDP'])
    print(merged_gdp_sort)
    test_plot_highest_gdp_10(merged, world)
    test_plot_lowest_gdp_10(merged, world)


if __name__ == '__main__':
    main()
