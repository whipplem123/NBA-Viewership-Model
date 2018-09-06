import pandas as pd
from datetime import datetime
from pandas.tseries.holiday import USFederalHolidayCalendar
from sklearn import linear_model
import csv

# NOTE: Change these as needed
game_data_file = "C:\\Users\\mw057599\\PycharmProjects\\nba_hackathon\\Q2\\game_data.csv"
player_data_file = "C:\\Users\\mw057599\\PycharmProjects\\nba_hackathon\\Q2\\player_data.csv"
training_set_file = "C:\\Users\\mw057599\\PycharmProjects\\nba_hackathon\\Q2\\training_set.csv"
test_set_file = "C:\\Users\\mw057599\\PycharmProjects\\nba_hackathon\\Q2\\test_set.csv"

# Sources:
# https://en.wikipedia.org/wiki/List_of_North_American_metropolitan_areas_by_population
# https://en.wikipedia.org/wiki/List_of_metropolitan_statistical_areas
# Metropolitan area population in millions
market_size_dict = {
    'NYK': 20.182305,
    'BKN': 20.182305,
    'LAL': 13.340068,
    'LAC': 13.340068,
    'CHI': 9.551031,
    'DAL': 7.102796,
    'HOU': 6.656947,
    'TOR': 6.129934,
    'WAS': 6.097684,
    'PHI': 6.069875,
    'MIA': 6.012331,
    'ATL': 5.710795,
    'BOS': 4.774321,
    'GSW': 4.656132,
    'PHX': 4.574531,
    'DET': 4.302043,
    'MIN': 3.524583,
    'DEN': 2.814330,
    'CHA': 2.426363,
    'POR': 2.389228,
    'ORL': 2.387138,
    'SAS': 2.384075,
    'SAC': 2.274194,
    'CLE': 2.060810,
    'IND': 1.988817,
    'MIL': 1.576236,
    'OKC': 1.383737,
    'MEM': 1.348260,
    'NOP': 1.275762,
    'UTA': 1.203105
}

# Source: https://www.statista.com/statistics/240386/twitter-followers-of-national-basketball-association-teams/
# Twitter followers in millions for each NBA team account
twitter_followers_dict = {
    'LAL': 7.39,
    'GSW': 5.63,
    'MIA': 4.68,
    'CHI': 4.09,
    'SAS': 3.32,
    'BOS': 3.21,
    'CLE': 3.16,
    'OKC': 2.55,
    'HOU': 2.54,
    'NYK': 2.07,
    'ORL': 1.59,
    'TOR': 1.5,
    'DAL': 1.48,
    'PHI': 1.46,
    'LAC': 1.37,
    'ATL': 1.19,
    'POR': 1.13,
    'IND': 1.11,
    'PHX': 0.99,
    'SAC': 0.96,
    'MEM': 0.92,
    'BKN': 0.88,
    'CHA': 0.88,
    'MIL': 0.87,
    'MIN': 0.85,
    'WAS': 0.85,
    'DET': 0.85,
    'NOP': 0.8,
    'UTA': 0.79,
    'DEN': 0.79
}

# Load data
game_data_df = pd.read_csv(game_data_file, sep=',', header=0)
game_data = game_data_df.values
player_data_df = pd.read_csv(player_data_file, sep=',', header=0)
player_data = player_data_df.values
training_set_df = pd.read_csv(training_set_file, sep=',', header=0)
training_set = training_set_df.values
test_set_df = pd.read_csv(test_set_file, sep=',', header=0)
test_set = test_set_df.values

print("Getting total viewers")

# Convert to datetime
for i in range(len(test_set)):
    test_set[i][2] = datetime.strptime(test_set[i][2], '%m/%d/%Y').date()

# Get total viewers
game_id = training_set[0][1]
total_viewers = 0
array = []
for i in range(len(training_set)):
    if training_set[i][1] != game_id:
        array.append([training_set[i - 1][0], training_set[i - 1][1], datetime.strptime(training_set[i - 1][2],
                    '%m/%d/%Y').date(), training_set[i - 1][3], training_set[i - 1][4], total_viewers])
        total_viewers = 0
        game_id = training_set[i][1]
    else:
        total_viewers += training_set[i][6]

i = len(training_set) - 1
array.append([training_set[i - 1][0], training_set[i - 1][1], datetime.strptime(training_set[i - 1][2],
            '%m/%d/%Y').date(), training_set[i - 1][3], training_set[i - 1][4], total_viewers])

training_set = array

print("Getting active all-stars")
# Get active all-stars
array = []
for game in training_set:
    all_stars = 0
    rows = [row for row in player_data if row[1] == game[1]]
    for row in rows:
        if row[6] != 'None' and row[7] == 'Active':
            all_stars += 1

    array.append([game[0], game[1], game[2], game[3], game[4], all_stars, game[5]])

training_set = array

array = []
for game in test_set:
    all_stars = 0
    rows = [row for row in player_data if row[1] == game[1]]
    for row in rows:
        if row[6] != 'None' and row[7] == 'Active':
            all_stars += 1

    array.append([game[0], game[1], game[2], game[3], game[4], all_stars])

test_set = array

print("Getting win percentages")
# Get win percentages
array = []
for game in training_set:
    rows = [row for row in game_data if row[1] == game[1]]
    home_pct = 0.0
    away_pct = 0.0
    for row in rows:
        if row[4] == 'H':
            if row[5] == row[6] == 0:
                home_pct = 0.0
            else:
                home_pct = row[5] / (row[5] + row[6])
        elif row[4] == 'A':
            if row[5] == row[6] == 0:
                away_pct = 0.0
            else:
                away_pct = row[5] / (row[5] + row[6])

    best_win_pct = max(home_pct, away_pct)
    avg_win_pct = (home_pct + away_pct) / 2
    array.append([game[0], game[1], game[2], game[3], game[4], game[5], best_win_pct, avg_win_pct, game[6]])

training_set = array

array = []
for game in test_set:
    rows = [row for row in game_data if row[1] == game[1]]
    home_pct = 0.0
    away_pct = 0.0
    for row in rows:
        if row[4] == 'H':
            if row[5] == row[6] == 0:
                home_pct = 0.5
            else:
                home_pct = row[5] / (row[5] + row[6])
        elif row[4] == 'A':
            if row[5] == row[6] == 0:
                away_pct = 0.5
            else:
                away_pct = row[5] / (row[5] + row[6])

    best_win_pct = max(home_pct, away_pct)
    avg_win_pct = (home_pct + away_pct) / 2
    array.append([game[0], game[1], game[2], game[3], game[4], game[5], best_win_pct, avg_win_pct])

test_set = array
print("Getting team popularity")

# Get team popularity
array = []
for game in training_set:
    total_market_size = market_size_dict[game[3]] + market_size_dict[game[4]]
    total_twitter_followers = twitter_followers_dict[game[3]] + twitter_followers_dict[game[4]]
    array.append([game[0], game[1], game[2], game[3], game[4], game[5], game[6], game[7], total_market_size,
                  total_twitter_followers, game[8]])

training_set = array

array = []
for game in test_set:
    total_market_size = market_size_dict[game[3]] + market_size_dict[game[4]]
    total_twitter_followers = twitter_followers_dict[game[3]] + twitter_followers_dict[game[4]]
    array.append([game[0], game[1], game[2], game[3], game[4], game[5], game[6], game[7], total_market_size,
                  total_twitter_followers])

test_set = array

print("Getting weekend/holiday")
# Determine whether game is played on weekend/holiday
holidays = USFederalHolidayCalendar().holidays(start='2016-01-01', end='2018-12-31').to_pydatetime()
holidays = [holiday.date() for holiday in holidays]
array = []
for game in training_set:
    date = game[2]
    weekend_or_holiday = 0
    if date in holidays or 4 <= date.weekday() <= 6:
        weekend_or_holiday = 1

    array.append([game[0], game[1], game[2], game[3], game[4], game[5], game[6], game[7], game[8], game[9],
                  weekend_or_holiday, game[10]])

training_set = array

array = []
for game in test_set:
    date = game[2]
    weekend_or_holiday = 0
    if date in holidays or 4 <= date.weekday() <= 6:
        weekend_or_holiday = 1

    array.append([game[0], game[1], game[2], game[3], game[4], game[5], game[6], game[7], game[8], game[9],
                  weekend_or_holiday])

test_set = array

# Fit linear model
independent_variables = []
dependent_variables = []

for game in training_set:
    independent_variables.append([game[5], game[6], game[7], game[8], game[9], game[10]])
    dependent_variables.append(game[11])

reg = linear_model.LinearRegression()
reg.fit(independent_variables, dependent_variables)

coef = reg.coef_

with open('test_set_Matt_Whipple.csv', 'w') as output_file:
    writer = csv.writer(output_file, dialect='excel', lineterminator='\n')
    row = ['Season', 'Game_ID', 'Game_Date', 'Away_Team', 'Home_Team', 'Total_Viewers']
    writer.writerow(row)
    for game in test_set:
        prediction = 0
        for i in range(len(coef)):
            prediction += coef[i] * game[i + 5]

        row = [game[0], game[1], game[2].strftime('%m/%d/%Y').lstrip('0').replace('/0', '/'), game[3], game[4], int(prediction)]
        writer.writerow(row)