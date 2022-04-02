from bs4 import BeautifulSoup
import requests
import csv

teamNamesMascot = {'Gonzaga Bulldogs': 1211, 'Arizona Wildcats': 1112, 'Kansas Jayhawks': 1242, 'Baylor Bears': 1124, 'Auburn Tigers': 1120, 'Kentucky Wildcats': 1246, 'Villanova Wildcats': 1437, 'Duke Blue Devils': 1181, 'Wisconsin Badgers': 1458, 'Tennessee Volunteers': 1397, 'Purdue Boilermakers': 1345, 'Texas Tech Red Raiders': 1403, 'UCLA Bruins': 1417, 'Illinois Fighting Illini': 1228, 'Providence Friars': 1344, 'Arkansas Razorbacks': 1116, 'UConn Huskies': 1163, 'Houston Cougars': 1222, 'Saint Mary\'s Gaels': 1388, 'Iowa Hawkeyes': 1234, 'Alabama Crimson Tide': 1104, 'LSU Tigers': 1261, 'Texas Longhorns': 1400, 'Colorado State Rams': 1161, 'USC Trojans': 1425, 'Murray State Racers': 1293, 'Michigan State Spartans': 1277, 'Ohio State Buckeyes': 1326, 'Boise State Broncos': 1129, 'North Carolina Tar Heels': 1314, 'San Diego State Aztecs': 1361, 'Seton Hall Pirates': 1371, 'Creighton Bluejays': 1166, 'TCU Horned Frogs': 1395, 'Marquette Golden Eagles': 1266, 'Memphis Tigers': 1272, 'San Francisco Dons': 1362, 'Miami Hurricanes': 1274, 'Loyola Chicago Ramblers': 1260, 'Davidson Wildcats': 1172, 'Iowa State Cyclones': 1235, 'Michigan Wolverines': 1276, 'Wyoming Cowboys': 1461, 'Rutgers Scarlet Knights': 1353, 'Indiana Hoosiers': 1231, 'Virginia Tech Hokies': 1439, 'Notre Dame Fighting Irish': 1323, 'UAB Blazers': 1412, 'Richmond Spiders': 1350, 'New Mexico State Aggies': 1308, 'Chattanooga Mocs': 1151, 'South Dakota State Jackrabbits': 1355, 'Vermont Catamounts': 1436, 'Akron Zips': 1103, 'Longwood Lancers': 1255, 'Yale Bulldogs': 1463, 'Colgate Raiders': 1159, 'Montana State Bobcats': 1286, 'Delaware Blue Hens': 1174, 'Saint Peter\'s Peacocks': 1389, 'Jacksonville State Gamecocks': 1240, 'CSU Fullerton Titans': 1168, 'Georgia State Panthers': 1209, 'Norfolk State Spartans': 1313, 'Wright State Raiders': 1460, 'Bryant Bulldogs': 1136, 'Texas Southern Tigers': 1411, 'Texas A&M-CC Islanders': 1394}
tourney_team_cards = []
dict = {}

main_page = requests.get('https://www.espn.com/mens-college-basketball/teams').text

soup = BeautifulSoup(main_page, 'lxml')
team_cards = soup.find_all('div', class_='mt3')

for teams in team_cards:
    team_name = teams.section.div.a.h2.text
    if team_name in teamNamesMascot:
        tourney_team_cards.append(teams)

main_url = "https://www.espn.com"

with open('2022RegularSeason.csv', 'w', newline='') as csvfile:
    fieldnames = ['Season', 'DayNum', 'WTeamID', 'WScore', 'LTeamID', 'LScore', 'WLoc', 'NumOT', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA', 'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for team_card in tourney_team_cards:
        url = team_card.section.div.div.find_all('span')[1].a.get("href", None)
        team_page = requests.get(main_url + url).text
        team_soup = BeautifulSoup(team_page, 'lxml')
        table = team_soup.find('tbody', class_='Table__TBODY')
        rows = table.find_all('tr')
        index = 0
        for i in range(len(rows)):
            tds = rows[i].find_all('td')
            if len(tds) == 1 and tds[0].text == "Regular Season":
                index = i
                print(i)
                break
        for j in range(index + 2, len(rows)):
            tds = rows[j].find_all('td')
            if len(tds) > 3:
                tag = tds[1].div.find_all('span')
                neutral_text = tag[2].text.split(" ")
                neutral = len(neutral_text) > 1 and neutral_text[1] == "*"
                print(neutral)

                result_tag = tds[2].find_all('span')
                result_td = result_tag[1].a
                printed_result = result_tag[0].text.split('-')
                OT_arr = result_td.text.split(" ")
                num_ot = '0'
                if len(OT_arr[1]) > 0:
                    num_ot = OT_arr[1][0] if OT_arr[1][0] != 'O' else '1'
                print(num_ot)
                game_url = result_td.get("href", None)
                game_url_arr = game_url.split("/")
                game_id = game_url_arr[len(game_url_arr) - 1]
                if game_id not in dict and len(printed_result) == 1:
                    dict[game_id] = 1
                    print(game_id)
                    game_page = requests.get('https://www.espn.com/mens-college-basketball/matchup?gameId=' + str(game_id)).text
                    game_soup = BeautifulSoup(game_page, 'lxml')
                    score_header = game_soup.find('div', class_="competitors")

                    t1_wrapper = score_header.find('div', class_="team away")
                    t1_score = t1_wrapper.div.find('div', class_="score-container").div.text
                    print(t1_score)

                    t1_name_container = t1_wrapper.find('div', class_="team-container").find('div', class_="team-info-wrapper")
                    t1_name = ""
                    if t1_name_container.a:
                        t1_name_tags = t1_name_container.a.find_all('span')
                        t1_name = t1_name_tags[0].text + " " + t1_name_tags[1].text
                    t1_id = 0
                    if t1_name in teamNamesMascot:
                        t1_id = teamNamesMascot[t1_name]

                    t2_wrapper = score_header.find('div', class_="team home")
                    t2_score = t2_wrapper.div.find('div', class_="score-container").div.text
                    print(t2_score)

                    t2_name_container = t2_wrapper.find('div', class_="team-container").find('div', class_="team-info-wrapper")
                    t2_name = ""
                    if t2_name_container.a:
                        t2_name_tags = t2_name_container.a.find_all('span')
                        t2_name = t2_name_tags[0].text + " " + t2_name_tags[1].text
                    t2_id = 0
                    if t2_name in teamNamesMascot:
                        t2_id = teamNamesMascot[t2_name]

                    t1win = int(t1_score) > int(t2_score)

                    div = game_soup.find('div', class_="col-two")
                    tbl = div.find('table', class_="mod-data")
                    trs = tbl.tbody.find_all('tr')

                    FGS = trs[0].find_all('td')
                    t1FG = FGS[1].text.split("-")
                    t1FGM = t1FG[0].strip()
                    t1FGA = t1FG[1].strip()

                    t2FG = FGS[2].text.split("-")
                    t2FGM = t2FG[0].strip()
                    t2FGA = t2FG[1].strip()

                    threes = trs[2].find_all('td')
                    t13P = threes[1].text.split("-")
                    t13PM = t13P[0].strip()
                    t13PA = t13P[1].strip()

                    t23P = threes[2].text.split("-")
                    t23PM = t23P[0].strip()
                    t23PA = t23P[1].strip()

                    fts = trs[4].find_all('td')
                    t1ft = fts[1].text.split("-")
                    t1FTM = t1ft[0].strip()
                    t1FTA = t1ft[1].strip()

                    t2ft = fts[2].text.split("-")
                    t2FTM = t2ft[0].strip()
                    t2FTA = t2ft[1].strip()

                    ORB = trs[7].find_all('td')
                    t1OR = ORB[1].text.strip()
                    t2OR = ORB[2].text.strip()

                    DRB = trs[8].find_all('td')
                    t1DR = DRB[1].text.strip()
                    t2DR = DRB[2].text.strip()

                    AST = trs[10].find_all('td')
                    t1Ast = AST[1].text.strip()
                    t2Ast = AST[2].text.strip()

                    TO = trs[13].find_all('td')
                    t1TO = TO[1].text.strip()
                    t2TO = TO[2].text.strip()

                    STL = trs[11].find_all('td')
                    t1Stl = STL[1].text.strip()
                    t2Stl = STL[2].text.strip()

                    BLK = trs[12].find_all('td')
                    t1Blk = BLK[1].text.strip()
                    t2Blk = BLK[2].text.strip()

                    PF = trs[14].find_all('td')
                    t1PF = PF[1].text.strip()
                    t2PF = PF[2].text.strip()

                    if t1win:
                        writer.writerow({'Season': '2022', 'DayNum': j, 'WTeamID': t1_id, 'WScore': t1_score, 'LTeamID': t2_id, 'LScore': t2_score, 'WLoc': 'N' if neutral else 'A', 'NumOT': num_ot, 'WFGM': t1FGM, 'WFGA': t1FGA, 'WFGM3': t13PM, 'WFGA3': t13PA, 'WFTM': t1FTM, 'WFTA': t1FTA, 'WOR': t1OR, 'WDR': t1DR, 'WAst': t1Ast, 'WTO': t1TO, 'WStl': t1Stl, 'WBlk': t1Blk, 'WPF': t1PF, 'LFGM': t2FGM, 'LFGA': t2FGA, 'LFGM3': t23PM, 'LFGA3': t23PA, 'LFTM': t2FTM, 'LFTA': t2FTA, 'LOR': t2OR, 'LDR': t2DR, 'LAst': t2Ast, 'LTO': t2TO, 'LStl': t2Stl, 'LBlk': t2Blk, 'LPF': t2PF})
                    else:
                        writer.writerow({'Season': '2022', 'DayNum': j, 'WTeamID': t2_id, 'WScore': t2_score, 'LTeamID': t1_id, 'LScore': t1_score, 'WLoc': 'N' if neutral else 'H', 'NumOT': num_ot, 'WFGM': t2FGM, 'WFGA': t2FGA, 'WFGM3': t23PM, 'WFGA3': t23PA, 'WFTM': t2FTM, 'WFTA': t2FTA, 'WOR': t2OR, 'WDR': t2DR, 'WAst': t2Ast, 'WTO': t2TO, 'WStl': t2Stl, 'WBlk': t2Blk, 'WPF': t2PF, 'LFGM': t1FGM, 'LFGA': t1FGA, 'LFGM3': t13PM, 'LFGA3': t13PA, 'LFTM': t1FTM, 'LFTA': t1FTA, 'LOR': t1OR, 'LDR': t1DR, 'LAst': t1Ast, 'LTO': t1TO, 'LStl': t1Stl, 'LBlk': t1Blk, 'LPF': t1PF})





    








