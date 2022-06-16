"""
This script takes in statistical and team data from nba.com and
given a season, find the top 5 and bottom 5 teams from that year
and calculates the number of back to back games each team had that
year as well as the win percentage of back to back games and non back
to back games. Generates a dataframe in order to evaluate the schedule
difficulty of back to back games.
"""
from nba_api.stats.endpoints import TeamGameLog
from nba_api.stats.endpoints import LeagueStandings
from nba_api.stats.static import teams
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()


def create_gamelog(city, season):
    """
    takes a city and season, and returns a pandas dataframe containing
    team statistical performance in major categories from that season
    returns an error if the city or season are unlisted or out of range
    parameters:
    city: str of name of city of the team of interest
    season: str of season of interest; format: "yyYY-{YY+1}", eg '2010-11'
    returns:
    pandas dataframe game log of the season with relevant stats and info
    """
    my_team = teams.find_teams_by_city(city)[0]
    my_team_id = my_team['id']
    team_season = TeamGameLog(team_id=my_team_id, season=season)
    gamelog_df = team_season.get_data_frames()[0]
    # note: the games are listed in reverse order, such that the most recent
    # game, the last game of the season, is at row 0.
    gamelog_df['Team'] = city.upper()
    gamelog_df['Season'] = season
    gamelog_df['GAME_DATE'] = pd.to_datetime(gamelog_df['GAME_DATE'],
                                             format='%b %d, %Y')
    gamelog_df['days_since_game'] = -(gamelog_df['GAME_DATE'].diff().shift(-1).
                                      apply(lambda x: x.days))
    return gamelog_df


def back_to_backs(data):
    """
    Takes in a gamelog dataframe for a single team and calculates the number of
    back to back games, total win percentage, the win percentage of all back to
    back games and the win percentage of games that are not back to back.
    Returns a list of all calculated stats along with the team name.
    """
    back_to_back_win_mask = (data['days_since_game'] == 1) & \
                            (data['WL'] == 'W')
    non_back_to_back_win_mask = (data['days_since_game'] != 1) & \
                                (data['WL'] == 'W')

    back_to_back_wins = len(data[back_to_back_win_mask])
    num_of_back_to_backs = len(data[data['days_since_game'] == 1])

    wins_not_back_to_back = len(data[non_back_to_back_win_mask])
    num_non_back_to_back = len(data[data['days_since_game'] != 1])

    team_name = data.loc[0, 'Team']
    season = data.loc[0, 'Season']
    back_to_back_win_pct = back_to_back_wins / num_of_back_to_backs
    winpct_not_back_to_back = wins_not_back_to_back / num_non_back_to_back
    total_winpct = data.loc[0, 'W_PCT']

    result = [team_name, season, total_winpct, back_to_back_win_pct,
              winpct_not_back_to_back, num_of_back_to_backs]

    return result


def find_top_bottom_10_teams(season):
    """
    Takes in a season (year) and finds the top 5 teams and bottom 5 teams
    that year based on win percentage. Returns a total of 10 teams, top 5 and
    bottom 5, in a list.
    """
    season_standings = LeagueStandings(season=season)
    standings_df = season_standings.get_data_frames()[0]
    top_five = standings_df.nlargest(5, columns='WinPCT')
    bottom_five = standings_df.nsmallest(5, columns='WinPCT')
    combined = pd.concat([top_five, bottom_five])

    return combined['TeamCity'].tolist()


def compare(season):
    """
    Takes in a list of lists of back to back game stats from different teams
    and combines and returns them in a pandas dataframe
    """
    top_bottom_10_teams = find_top_bottom_10_teams(season)
    seasons_gamelogs = [create_gamelog(team, season) for team in
                        top_bottom_10_teams]
    back_to_back_stats = [back_to_backs(gamelog) for gamelog in
                          seasons_gamelogs]
    df = pd.DataFrame(back_to_back_stats,
                      columns=['Team', 'Season', 'Total_WinPct',
                               'Back_to_Back_WinPct',
                               'Non_Back_to_Back_WinPct',
                               'Num_Back_to_Backs'])
    return df


def merge_seasons(data1, data2, data3):
    """
    Takes in 3 back to back game data season dataframes and
    merges them and returns it as one dataframe
    """
    seasons = [data1, data2, data3]
    combined = pd.concat(seasons)
    return combined


def average(back_to_back_df):
    """
    Takes in a single back to back game data dataframe and calculates
    prints out the average stats for each category
    """
    avg_back_to_back_winpct = back_to_back_df['Back_to_Back_WinPct'].mean()
    avg_non_back_to_back_winpct = back_to_back_df[
                                  'Non_Back_to_Back_WinPct'].mean()
    avg_num_back_to_back = back_to_back_df['Num_Back_to_Backs'].mean()

    print('Average Back to Back Win Percentage',
          avg_back_to_back_winpct)
    print('Average Non Back to Back Win Percentage',
          avg_non_back_to_back_winpct)
    print('Average Number of Back to Back Games',
          avg_num_back_to_back)


def plot_avg_back_to_back_winpct(df):
    """
    Takes in a dataframe of back to back games from multiple seasons
    and plots the back to back win percentage as a bar graph
    """
    season = df.groupby('Season')['Back_to_Back_WinPct'].mean()
    season_avg_df = pd.DataFrame({'Season': season.index,
                                 'Back_to_Back_WinPct': season.values})

    sns.catplot(data=season_avg_df, x='Season', y='Back_to_Back_WinPct',
                kind='bar')
    plt.title('Back-To-Back Win Percentage Per Season')
    plt.ylabel('Back-to-Back Win Percentage')
    plt.savefig('back_to_back_winpct.png')


def plot_avg_non_back_to_back_winpct(df):
    """
    Takes in a dataframe of back to back games from multiple seasons
    and plots the non back to back win percentage as a bar graph
    """
    season = df.groupby('Season')['Non_Back_to_Back_WinPct'].mean()
    season_avg_df = pd.DataFrame({'Season': season.index,
                                 'Non_Back_to_Back_WinPct': season.values})

    sns.catplot(data=season_avg_df, x='Season', y='Non_Back_to_Back_WinPct',
                kind='bar')
    plt.title('Non Back-To-Back Win Percentage Per Season')
    plt.ylabel('Non Back-to-Back Win Percentage')
    plt.savefig('non_back_to_back_winpct.png')


def main():
    season_16_17 = compare('2016-17')
    season_17_18 = compare('2017-18')
    season_18_19 = compare('2018-19')

    print(season_16_17)
    average(season_16_17)

    combined_df = merge_seasons(season_16_17, season_17_18, season_18_19)

    plot_avg_back_to_back_winpct(combined_df)
    plot_avg_non_back_to_back_winpct(combined_df)


if __name__ == "__main__":
    main()
