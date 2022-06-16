"""
This script runs some basic tests on the game log dataframes generated in the
main script and compares their values with manually verified or computed values
to ensure that the outputs are correct
"""

from helper_func import assert_equals
from nba_predictor import load_in_data, concatenate


def test_load_in_data(data_test):
    """
    This function tests the method called load_in_data by comparing manually
    searched stats from a certain team.
    """

    assert_equals(116.6, data_test.loc[0, ['PTS']])
    assert_equals(14.4, data_test.loc[1, ['TOV']])
    assert_equals(19.3, data_test.loc[2, ['PF']])
    assert_equals('Los Angeles Lakers', data_test.loc[3, ['Team']][0])


def test_concatenate(data):
    """
    This function tests the method called concatenate by comparing manually
    searched stats from a certain team.
    """

    assert_equals(88.3, data[data['PTS'] == 113.4]['FGA'])
    assert_equals(84.0, data[data['3P%'] == 0.339]['FGA'])
    assert_equals(84.8, data[data['FG%'] == 0.414]['FGA'])
    assert_equals(81.3, data[data['2PA'] == 64.9]['FGA'])


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
    data_test = load_in_data(
        '2020-21 NBA Standings.csv',
        'NBA team per game stats_20-21 season.csv')

    test_load_in_data(data_test)
    data = concatenate(
        data1, data2, data3, data4, data5, data6, data7, data8, data9, data10)
    test_concatenate(data)


if __name__ == "__main__":
    main()
