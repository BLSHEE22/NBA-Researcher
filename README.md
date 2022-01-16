# NBA-Researcher
Search for specific NBA games, happenings, and patterns from 2004-2021 (March 2021).

There are seven parameters that can be filled out to narrow down a search:

1. year: games from a certain year
2. month: games from a certain month
3. day: games from a certain day
4. home_team: games with a certain home team
5. away_team: games with a certain away team
6. winReason: games won due to a certain statistical difference 
  - Answer in the format "home:STAT" or "away:STAT"
  - A "stat" can be any of the following:
  - ("PTS","FGM","FGA","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT","OREB","DREB",
  - "REB","AST", "STL","BLK","TO","PF","+/-")
  - Answering "any" anywhere will tell the engine not to specify in that department
  - E.g. "home:REB", "home:any", "any:REB"
  - Note: Entering a winReason parameter MUST be accompanied by another search parameter
7. ptpr: short for "Player, Team, Performance, Result"
  - Answer in the format "PlayerName:Team:STAT(< or >)Number:(W or L)"
  - Answering "any" anywhere will tell the engine not to specify in that department
  - E.g. "Marcus Smart:Celtics:FGA>11:W", "any:Celtics:FGA>11:L", "Marcus Smart:any:any:any"
  - Use the below format to bring up all of a player's games:
  - "PlayerName:career"

Trends in the NBA can be discovered and analyzed, leading to player and team insights.

This is still a work in progress. The updates I am currently making are listed in the large comment section 
at the top of the python file. As of 6/7/21, anything about the NBA from 2004-2021 can be searched and studied.
I plan on re-implementing this search engine on a more visual framework in order to feature graphs that are able 
to display trends and correlations.

The databases come thanks to Nathan Lauga, who compiled each one using the nba.com/stats website.

https://www.kaggle.com/nathanlauga/nba-games?select=teams.csv

The CSV files from the site above must be downloaded and placed into a separate folder inside of the 
repository folder.

Run "boxscores.py" using the following command:

python3 boxscores.py CSV_folder_name

Have fun exploring NBA statistics!
