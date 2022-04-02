from bs4 import BeautifulSoup
import requests

teamNames = ['Gonzaga', 'Arizona', 'Kansas', 'Baylor', 'Auburn', 'Kentucky', 'Villanova', 'Duke', 'Wisconsin', 'Tennessee', 'Purdue', 'Texas Tech', 'UCLA', 'Illinois', 'Providence', 'Arkansas', 'UConn', 'Houston', 'Saint Mary\'s', 'Iowa', 'Alabama', 'LSU', 'Texas', 'Colorado St.', 'USC', 'Murray St.', 'Michigan State', 'Ohio State', 'Boise State', 'North Carolina', 'San Diego State', 'Seton Hall', 'Creighton', 'TCU', 'Marquette', 'Memphis', 'San Francisco', 'Miami', 'Loyola Chicago', 'Davidson', 'Iowa State', 'Michigan', 'Wyoming', 'Rutgers', 'Indiana', 'Virginia Tech', 'Notre Dame', 'UAB', 'Richmond', 'New Mexico State', 'Chattanooga', 'South Dakota', 'Vermont', 'Akron', 'Longwood', 'Yale', 'Colgate', 'Montana State', 'Delaware', 'Saint Peter\'s', 'Jacksonville State', 'CSU Fullerton', 'Georgia State', 'Norfolk State', 'Wright State', 'Bryant', 'Texas Southern', 'Texas A&M-CC']

teamNamesMascot = ['Gonzaga Bulldogs', 'Arizona Wildcats', 'Kansas Jayhawks', 'Baylor Bears', 'Auburn Tigers', 'Kentucky Wildcats', 'Villanova Wildcats', 'Duke Blue Devils', 'Wisconsin Badgers', 'Tennessee Volunteers', 'Purdue Boilermakers', 'Texas Tech Red Raiders', 'UCLA Bruins', 'Illinois Fighting Illini', 'Providence Friars', 'Arkansas Razorbacks', 'UConn Huskies', 'Houston Cougars', 'Saint Mary\'s Gaels', 'Iowa Hawkeyes', 'Alabama Crimson Tide', 'LSU Tigers', 'Texas Longhorns', 'Colorado State Rams', 'USC Trojans', 'Murray State Racers', 'Michigan State Spartans', 'Ohio State Buckeyes', 'Boise State Broncos', 'North Carolina Tar Heels', 'San Diego State Aztecs', 'Seton Hall Pirates', 'Creighton Bluejays', 'TCU Horned Frogs', 'Marquette Golden Eagles', 'Memphis Tigers', 'San Francisco Dons', 'Miami Hurricanes', 'Loyola Chicago Ramblers', 'Davidson Wildcats', 'Iowa State Cyclones', 'Michigan Wolverines', 'Wyoming Cowboys', 'Rutgers Scarlet Knights', 'Indiana Hoosiers', 'Virginia Tech Hokies', 'Notre Dame Fighting Irish', 'UAB Blazers', 'Richmond Spiders', 'New Mexico State Aggies', 'Chattanooga Mocs', 'South Dakota State Jackrabbits', 'Vermont Catamounts', 'Akron Zips', 'Longwood Lancers', 'Yale Bulldogs', 'Colgate Raiders', 'Montana State Bobcats', 'Delaware Blue Hens', 'Saint Peter\'s Peacocks', 'Jacksonville State Gamecocks', 'CSU Fullerton Titans', 'Georgia State Panthers', 'Norfolk State Spartans', 'Wright State Raiders', 'Bryant Bulldogs', 'Texas Southern Tigers', 'Texas A&M-CC Islanders']
tourney_team_cards = []

def contains(name):
    for _name in teamNamesMascot:
        if(_name == name): 
            return True
    return False

def contains2():
    for _name in teamNamesMascot:
        found = False
        for _team in tourney_team_cards:
            if(_name == _team.section.div.a.h2.text): 
                found = True
        if not found:
            print(_name) 

main_page = requests.get('https://www.espn.com/mens-college-basketball/teams').text

soup = BeautifulSoup(main_page, 'lxml')
team_cards = soup.find_all('div', class_='mt3')



for teams in team_cards:
    team_name = teams.section.div.a.h2.text
    if(contains(team_name)):
        tourney_team_cards.append(teams)

for teams in tourney_team_cards:
    print(teams.section.div.a.h2.text)

print(len(tourney_team_cards))
print(len(teamNamesMascot))

contains2()
    








