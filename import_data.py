import pandas as pd
import time


# SoS Calculation
def SoS_calc(input_df, output_df, year_range):  # input_df is the game by game df, output_df is the team_avgs df

    sos_dict = {}
    input_df['Season'] = pd.to_numeric(input_df['Season'])

    for year in year_range:
        working_df = input_df[input_df['Season'] == year]
        working_df = working_df.filter(["WTeamID", "LTeamID"])

        for row in working_df.itertuples(index=False):
            winner = int(row[0])
            loser = int(row[1])

            if winner not in sos_dict:
                temp_sos = {"opp_list": [loser], "wins": 1, "losses": 0, "win%": 0, "ow%": 0, "oow%": 0, "sos": 0}
                sos_dict[winner] = temp_sos.copy()
                temp_sos.clear()
            else:
                sos_dict[winner]["opp_list"].append(loser)
                sos_dict[winner]["wins"] += 1

            if loser not in sos_dict:
                temp_sos = {"opp_list": [winner], "wins": 0, "losses": 1, "win%": 0, "ow%": 0, "oow%": 0, "sos": 0}
                sos_dict[loser] = temp_sos.copy()
                temp_sos.clear()
            else:
                sos_dict[loser]["opp_list"].append(winner)
                sos_dict[loser]["losses"] += 1

        for calc in ["win%", "ow%", "oow%", "sos"]:
            for k, d in sos_dict.items():
                if calc == "win%":
                    d["win%"] = d["wins"] / (d["wins"] + d["losses"])

                if calc == "ow%":
                    sum_wp = 0
                    num = 0
                    for opp in d["opp_list"]:
                        sum_wp += sos_dict[opp]["win%"]
                        num += 1
                    d["ow%"] = (sum_wp / num)

                if calc == "oow%":
                    sum_ow = 0
                    num = 0
                    for opp in d["opp_list"]:
                        sum_ow += sos_dict[opp]["ow%"]
                        num += 1
                    d["oow%"] = (sum_ow / num)
                    d["sos"] = (d["ow%"] * 2 + d["oow%"]) / 3

        sos_year_df = output_df[output_df["Season"] == year]
        team_list = sos_year_df["TeamID"].tolist()
        for row in output_df[output_df["Season"] == year].itertuples():
            output_df.iat[row.Index, output_df.columns.get_loc("SOS")] = sos_dict[row[2]]["sos"]

        sos_dict.clear()

    return output_df

def import_legacy(cols, years):
    # for runtime
    start_time = time.time()

    # import the regular season data (from same directory as this file)
    temp_df = pd.read_csv("./MRegularSeasonDetailedResults.csv",
                          names=['Season', 'DayNum', 'WTeamID', 'WScore', 'LTeamID', 'LScore', 'WLoc', 'NumOT', 'WFGM',
                                 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk',
                                 'WPF', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR', 'LDR', 'LAst', 'LTO',
                                 'LStl', 'LBlk', 'LPF'],
                          encoding="ISO-8859-1",
                          low_memory=False)

    # import tournament data (from same directory as this file)
    tourney_temp_df = pd.read_csv("./MNCAATourneyDetailedResults.csv",
                                  names=['Season', 'DayNum', 'WTeamID', 'WScore', 'LTeamID', 'LScore', 'WLoc', 'NumOT',
                                         'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR', 'WAst', 'WTO',
                                         'WStl', 'WBlk', 'WPF', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR',
                                         'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'],
                                  encoding="ISO-8859-1")

    # import seed data (from same directory as this file)
    seeds_df = pd.read_csv("./MNCAATourneySeeds.csv",
                           names=['Season', 'Seed', 'TeamID'],
                           encoding="ISO-8859-1")

    # drop headers from dfs
    reg_season_df = temp_df.drop(labels=0, axis=0)
    tourney_df = tourney_temp_df.drop(labels=0, axis=0)
    seeds_df = seeds_df.drop(labels=0, axis=0)

    # initialize team_avgs dataframe to be filled
    team_avgs = pd.DataFrame(columns=cols)

    # make sure 'Season" column and 'TeamID' columns are all numerics
    reg_season_df['Season'] = pd.to_numeric(reg_season_df['Season'])
    tourney_df['Season'] = pd.to_numeric(tourney_df['Season'])
    seeds_df['Season'] = pd.to_numeric(seeds_df['Season'])
    seeds_df['TeamID'] = pd.to_numeric(seeds_df['TeamID'])

    # loop through years to get team average stats season-by-season
    for year in years:
        year_df = reg_season_df[reg_season_df['Season'] == year]
        tourney_year_df = tourney_df[tourney_df['Season'] == year]
        dictionary = {}
        for index, row in tourney_year_df.iterrows():
            # print(row['WTeamID'])
            dictionary[int(row['WTeamID'])] = 1
            dictionary[int(row['LTeamID'])] = 1

        for key in dictionary:
            team_W = year_df[year_df['WTeamID'].apply(pd.to_numeric) == key]
            team_L = year_df[year_df['LTeamID'].apply(pd.to_numeric) == key]

            team_W_df = team_W[
                ['Season', 'WTeamID', 'WScore', 'LScore', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR',
                 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF']].apply(pd.to_numeric)
            team_L_df = team_L[
                ['Season', 'LTeamID', 'LScore', 'WScore', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR',
                 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']].apply(pd.to_numeric)

            w_sum = team_W_df.sum(axis=0, numeric_only=True)

            l_sum = {'Season': 0, 'LTeamID': 0, 'LScore': 0, 'WScore': 0, 'LFGM': 0, 'LFGA': 0, 'LFGM3': 0, 'LFGA3': 0,
                     'LFTM': 0, 'LFTA': 0, 'LOR': 0, 'LDR': 0, 'LAst': 0, 'LTO': 0, 'LStl': 0, 'LBlk': 0, 'LPF': 0}
            if not team_L.empty:
                l_sum = team_L_df.sum(axis=0, numeric_only=True)

            # calculate the team averages
            tot_games = (len(team_W_df.index) + len(team_L_df.index))

            season_total = (w_sum['Season'] + l_sum['Season']) / tot_games

            id_total = (w_sum['WTeamID'] + l_sum['LTeamID']) / tot_games
            score_total = (w_sum['WScore'] + l_sum['LScore']) / tot_games
            pa_total = (w_sum['LScore'] + l_sum['WScore']) / tot_games
            rebs_total = (w_sum['WOR'] + l_sum['LOR'] + w_sum['WDR'] + l_sum['LDR']) / tot_games
            ast_total = (w_sum['WAst'] + l_sum['LAst']) / tot_games
            stl_total = (w_sum['WStl'] + l_sum['LStl']) / tot_games
            blk_total = (w_sum['WBlk'] + l_sum['LBlk']) / tot_games
            pf_total = (w_sum['WPF'] + l_sum['LPF']) / tot_games
            to_total = (w_sum['WTO'] + l_sum['LTO']) / tot_games
            fgp_total = ((w_sum['WFGM'] + l_sum['LFGM']) / (w_sum['WFGA'] + l_sum['LFGA']))

            sos_temp = 0
            team_avgs.loc[len(team_avgs.index)] = [season_total, id_total, len(team_W_df.index),
                                                   len(team_L_df.index), score_total, pa_total, rebs_total,
                                                   ast_total, stl_total, blk_total, pf_total, to_total, sos_temp,
                                                   fgp_total]

    team_avgs = SoS_calc(reg_season_df, team_avgs, years)

    runtime = time.time() - start_time
    return runtime, team_avgs, reg_season_df, tourney_df, seeds_df


def import_year(cols):
    # for runtime
    start_time = time.time()

    # regular season 2022
    reg_2022_df = pd.read_csv("./2022RegularSeason.csv",
                              names=['Season', 'DayNum', 'WTeamID', 'WScore', 'LTeamID', 'LScore', 'WLoc', 'NumOT',
                                     'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR', 'WAst', 'WTO',
                                     'WStl', 'WBlk', 'WPF', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR',
                                     'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF'],
                              encoding="ISO-8859-1",
                              low_memory=False)
    reg_2022_df = reg_2022_df.drop(labels=0, axis=0)
    tourney_team_ids = [1211, 1112, 1242, 1124, 1120, 1246, 1437, 1181, 1458, 1397, 1345, 1403, 1417, 1228, 1344, 1116,
                        1163, 1222, 1388, 1234, 1104, 1261, 1400, 1161, 1425, 1293, 1277, 1326, 1129, 1314, 1361, 1371,
                        1166, 1395, 1266, 1272, 1362, 1274, 1260, 1172, 1235, 1276, 1461, 1353, 1231, 1439, 1323, 1412,
                        1350, 1308, 1151, 1355, 1436, 1103, 1255, 1463, 1159, 1286, 1174, 1389, 1240, 1168, 1209, 1313,
                        1460, 1136, 1411, 1394]
    team_avgs_2022 = pd.DataFrame(columns=cols)

    for key in tourney_team_ids:
        team_wins = reg_2022_df[reg_2022_df['WTeamID'] == str(key)]
        team_losses = reg_2022_df[reg_2022_df['LTeamID'] == str(key)]

        team_win_df = team_wins[
            ['Season', 'WTeamID', 'WScore', 'LScore', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR',
             'WAst', 'WTO', 'WStl', 'WBlk', 'WPF']].apply(pd.to_numeric)
        team_loss_df = team_losses[
            ['Season', 'LTeamID', 'LScore', 'WScore', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR', 'LDR',
             'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']].apply(pd.to_numeric)

        w_sum = team_win_df.sum(axis=0, numeric_only=True)

        l_sum = {'Season': 0, 'LTeamID': 0, 'LScore': 0, 'LFGM': 0, 'LFGA': 0, 'LFGM3': 0, 'LFGA3': 0, 'LFTM': 0,
                 'LFTA': 0, 'LOR': 0, 'LDR': 0, 'LAst': 0, 'LTO': 0, 'LStl': 0, 'LBlk': 0, 'LPF': 0}
        if not team_losses.empty:
            l_sum = team_loss_df.sum(axis=0, numeric_only=True)

        tot_games = (len(team_win_df.index) + len(team_loss_df.index))
        season_total = (int(w_sum['Season']) + int(l_sum['Season'])) / tot_games
        id_total = (w_sum['WTeamID'] + l_sum['LTeamID']) / tot_games
        score_total = (w_sum['WScore'] + l_sum['LScore']) / tot_games
        pa_total = (w_sum['LScore'] + l_sum['WScore']) / tot_games
        rebs_total = (w_sum['WOR'] + l_sum['LOR'] + w_sum['WDR'] + l_sum['LDR']) / tot_games
        ast_total = (w_sum['WAst'] + l_sum['LAst']) / tot_games
        stl_total = (w_sum['WStl'] + l_sum['LStl']) / tot_games
        blk_total = (w_sum['WBlk'] + l_sum['LBlk']) / tot_games
        pf_total = (w_sum['WPF'] + l_sum['LPF']) / tot_games
        to_total = (w_sum['WTO'] + l_sum['LTO']) / tot_games
        fgp_total = ((w_sum['WFGM'] + l_sum['LFGM']) / (w_sum['WFGA'] + l_sum['LFGA']))
        sos_temp = 0

        team_avgs_2022.loc[len(team_avgs_2022.index)] = [season_total, id_total, len(team_win_df.index),
                                                         len(team_loss_df.index), score_total, pa_total, rebs_total,
                                                         ast_total, stl_total, blk_total, pf_total, to_total, sos_temp,
                                                         fgp_total]

    team_avgs_2022 = SoS_calc(reg_2022_df, team_avgs_2022, [2022])

    runtime = time.time() - start_time
    return runtime, team_avgs_2022, reg_2022_df
