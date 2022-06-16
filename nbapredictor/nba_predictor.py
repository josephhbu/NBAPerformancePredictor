"""
This program implements functions called load_in_data,
concatenate, ml_predict, ml_looping, and visualize_barchart
to analyze games in NBA and predict each teams' season standings.
"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import dataframe_image as dfi
import altair as alt
from altair_saver import save


def load_in_data(title1, title2):
    """
    Returns a data frame by merging two kinds of data frames after datasets are
    cleaned: NBA Standings and NBA team per game stats.

    parameters:
    title1: title of a first data frame
    title2: title of a second data frame
    """
    data1 = pd.read_csv(title1)
    data1_clean = data1[['Rk', 'Team']]

    data2 = pd.read_csv(title2)
    data2['Team'] = data2['Team'].str.replace("*", '', regex=True)
    # Dropping unnecessary variables that overlap and are
    # not related to standings.
    data2 = data2.drop(
        columns=['Rk', 'G', 'MP', 'FG', '3P', '2P', 'FT', 'TRB'])
    data2_clean = data2.drop(data2.index[30])

    merged = data1_clean.merge(data2_clean, left_on='Team', right_on='Team')

    return merged


def concatenate(
        data1, data2, data3, data4, data5, data6, data7, data8, data9, data10):
    """
    Returns a concatenated data frame to represent the last decade of
    NBA season.

    parameters:
    dataframe from a load_in_data
    """
    frames = [data1, data2, data3, data4, data5]
    result = pd.concat(frames)
    # After datasets are concatenated, the variable named 'Team' needs to be
    # removed as it is irrelevant in training the model.
    result = result.drop(columns=['Team'])

    return result


def ml_predict(data, test_data):
    """
    Returns the prediction of the season standing ranks.

    parameters:
    data: data to train
    test_data: data to test
    """
    test_data = test_data.drop(columns=['Team', 'Rk'])
    features = data.loc[:, data.columns != 'Rk']
    labels = data['Rk']

    model = DecisionTreeClassifier()
    model.fit(features, labels)
    predictions = model.predict(test_data)

    return predictions


def ml_looping(data, test_data):
    """
    Returns the average of the looped prediction results after
    a user inputs how many times it will run(loop) the prediction.

    parameters:
    data: parameter data for running ml_predict
    test_data: parameter data for running ml_predict
    """
    times = int(input("How many times do you want to run: "))
    array = np.zeros(30)
    count = 0

    for i in range(times):
        array += ml_predict(data, test_data)
        count += 1

    rank_score = array/times
    rank_average = np.around(rank_score, decimals=2)

    return rank_average


def final_dataframe(predictions, test_data):
    """
    Returns the final data frame showing each Team's name, rank and the
    rank score(average of looped prediction rank).

    parameters:
    predictions: prediction rank
    test_data: data frame to create final data frame
    """
    test_data['Rank Score'] = predictions
    test_data_clean = test_data[['Rank Score', 'Team']]
    test_data_clean = test_data_clean.copy()
    test_data_clean['Rank Score'] = test_data_clean['Rank Score'].astype(float)
    test_data_clean = test_data_clean.sort_values('Rank Score')
    test_data_clean['Rank'] = np.arange(start=1, stop=31)
    test_data_clean = test_data_clean[['Rank', 'Team', 'Rank Score']]

    return test_data_clean


def visualize_barchart(result, test_data):
    """
    Saves the bar chart showing the difference between predicted and
    actual season standings. Teams predicted higher will be represented in
    a steelblue color, while teams predicted lower will be represented in
    orange.

    parameters:
    result and test_data is needed in order to calculated the difference
    which is going to be visualized in this function.
    """
    rank = test_data['Rk']
    rank2 = result['Rank']
    difference = rank-rank2

    result['difference'] = difference

    chart = alt.Chart(result).mark_bar().encode(
        x="difference",
        y="Team",
        color=alt.condition(
            alt.datum.difference > 0,
            alt.value("steelblue"),
            alt.value("orange"))
        ).properties(
            title="The Difference between Predicted & Actual Season Standings",
            width=600)

    # The plot can be downloaded in other formats such as png after
    # it is opened in html format (Click the 'three dot' button on the
    # right top corner)
    save(chart, 'chart.html')


def main():
    data1 = load_in_data(
        '2019-20 NBA Standings.csv',
        'NBA team per game stats_19-20 season.csv')
    data2 = load_in_data(
        '2018-19 NBA Standings.csv',
        'NBA team per game stats_18-19 season.csv')
    data3 = load_in_data(
        '2017-18 NBA Standings.csv',
        'NBA team per game stats_17-18 season.csv')
    data4 = load_in_data(
        '2016-17 NBA Standings.csv',
        'NBA team per game stats_16-17 season.csv')
    data5 = load_in_data(
        '2015-16 NBA Standings.csv',
        'NBA team per game stats_15-16 season.csv')
    data6 = load_in_data(
        '2014-15 NBA Standings.csv',
        'NBA team per game stats_14-15 season.csv')
    data7 = load_in_data(
        '2013-14 NBA Standings.csv',
        'NBA team per game stats_13-14 season.csv')
    data8 = load_in_data(
        '2012-13 NBA Standings.csv',
        'NBA team per game stats_12-13 season.csv')
    data9 = load_in_data(
        '2011-12 NBA Standings.csv',
        'NBA team per game stats_11-12 season.csv')
    data10 = load_in_data(
        '2010-11 NBA Standings.csv',
        'NBA team per game stats_10-11 season.csv')

    data = concatenate(
        data1, data2, data3, data4, data5, data6, data7, data8, data9, data10)
    data_test = load_in_data(
        '2020-21 NBA Standings.csv',
        'NBA team per game stats_20-21 season.csv')

    looped_predictions = ml_looping(data, data_test)
    result = final_dataframe(looped_predictions, data_test)

    visualize_barchart(result, data_test)
    # exports the result of final data frame in png format
    dfi.export(result, 'df_styled.png')


if __name__ == '__main__':
    main()
