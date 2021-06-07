# NBA-Researcher
Search for specific NBA games, happenings, and patterns from 2004-2021 (March 2021).

There are seven parameters that can be filled out to narrow down a search:

1. year: games from a certain year
2. month: games from a certain month
3. day: games from a certain day
4. home_team: games with a certain home team
5. away_team: games with a certain away team
6. winReason: games won due to a certain statistical difference 
  - Answer in the format "home/away:stat"
  - Answering "any" anywhere will tell the engine not to specify in that department
  - E.g. "home:REB", "home:any", "any:REB"
7. playerPerformance: games where a certain player met certain criteria
  - Answer in the format "playerName:stat>number" (or <)
  - Answering "any" anywhere will tell the engine not to specify in that department
  - E.g. "Marcus Smart:FGA>11", "any:FGA>11", "Marcus Smart:any"

Trends in the NBA can be discovered and analyzed, leading to player and team insights.

This is still a work in progress. The updates I am currently making are listed in the large comment section 
inside the "welcome" function. As of 6/7/21, anything about the NBA from 2004-2021 can be searched and studied.
I plan on re-implementing this search engine on a more visual framework in order to feature graphs that are able 
to display trends and correlations.

The databases come thanks to Nathan Lauga, who compiled each one using the nba.com/stats website.

https://www.kaggle.com/nathanlauga/nba-games?select=teams.csv

Each CSV file from the site above must be downloaded and placed into a separate folder inside of the 
repository folder.

Have fun exploring NBA statistics!
