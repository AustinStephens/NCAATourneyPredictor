import pandas as pd
import time
import random
import warnings

import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn import svm


def randomize_winner(trim_tourney_df, team_avgs, train_cols, seeds_df, cols, years):

    warnings.filterwarnings("ignore", category=FutureWarning)

    random.seed()

    train_DF_temp = pd.DataFrame(columns=train_cols)
    for year in years:
        avg_year_df = team_avgs[team_avgs['Season'] == year]
        seeds_year_df = seeds_df[seeds_df['Season'] == year]
        tourney_year_df = trim_tourney_df[trim_tourney_df['Season'] == year].apply(pd.to_numeric)

        for index, row in tourney_year_df.iterrows():
            # make a list that we can insert into the new dataframe
            # first 4 values (last value is the "Winner" classification which is randomly chosen)
            team1_seed = seeds_year_df[seeds_year_df['TeamID'] == row["WTeamID"]].values.tolist()[0][1]
            team2_seed = seeds_year_df[seeds_year_df['TeamID'] == row["LTeamID"]].values.tolist()[0][1]
            team1_prefix = team1_seed[0:1]
            team2_prefix = team2_seed[0:1]

            team1_seed = int(team1_seed[1:3])
            team2_seed = int(team2_seed[1:3])

            # choose which team is first based on seed
            winning_team = 2
            losing_team = 1

            if team1_seed < team2_seed:
                winning_team = 1
                losing_team = 2
            elif team2_seed == team1_seed:
                if team1_prefix > team2_prefix:
                    winning_team = 1
                    losing_team = 2

            # properly put winning team into correct row
            team_id = ["", "WTeamID", "LTeamID"]
            temp_list = [year, row[team_id[winning_team]], row[team_id[losing_team]], winning_team]
            team1_row = avg_year_df[avg_year_df["TeamID"] == temp_list[1]][cols[2:]].values.tolist()
            team2_row = avg_year_df[avg_year_df["TeamID"] == temp_list[2]][cols[2:]].values.tolist()
            temp_list.extend(team1_row[0])
            temp_list.extend(team2_row[0])

            # add that list to our DF
            temp_series = pd.Series(temp_list, index=train_cols)
            train_DF_temp = train_DF_temp.append(temp_series, ignore_index=True)
    return train_DF_temp


def tourney_2022(team_ids, team_avgs_2022, test_cols):

    temp_tourn_df = pd.DataFrame(data=team_ids)
    # winners = [2,1,1,2,1,2,2,1,2,1,1,1,1,2,1,1,1,1,1,2,1,2,1,1,2,1,1,1,1,2,2,1,2,1,2,1,1,2,2,2,2,2,2,2,1,1,1,2,1,2,1,1,2,2,1,2,2,2,1,2,2,1,2,1,2,2,2]
    tourney_2022_df = pd.DataFrame(columns=test_cols)

    for row in temp_tourn_df.iterrows():
        # Doing the same as before but without winner column
        temp_list = [2022, row[1]['Team1ID'], row[1]['Team2ID']]
        #print(f"team2: ", row[1]['Team2ID'])
        team1_row = team_avgs_2022[team_avgs_2022["TeamID"] == row[1]['Team1ID']].values.tolist()
        team2_row = team_avgs_2022[team_avgs_2022["TeamID"] == row[1]['Team2ID']].values.tolist()
        #print(team2_row)
        team1_row[0].pop(0)
        team1_row[0].pop(0)
        team2_row[0].pop(0)
        team2_row[0].pop(0)

        temp_list.extend(team1_row[0])
        temp_list.extend(team2_row[0])

        # add that list to our DF
        temp_series = pd.Series(temp_list, index=test_cols)
        tourney_2022_df = tourney_2022_df.append(temp_series, ignore_index=True)

    return tourney_2022_df