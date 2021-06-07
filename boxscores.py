import csv
import sys
import math
import random
# import scipy.stats

# font colors
YELLOW = '\033[33m' 
GREEN = '\033[32m'
BGREEN = '\033[1;32m'
CYAN = '\033[1;36m'
RED = '\033[31m'
BRED = '\033[1;31m'
BOLDW = '\033[1;37m'
RESET = '\033[m'

# Reads the CSV files for train and test sets, returns list of examples
def read_csv(filename):
    rows = 0
    new_table = []
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        table = list(spamreader)
        # table.pop(0) #remove first row of CSV
    return table #list of lists

# how can I make specific searches? Ex. every time Marcus Smart shot over 11 times
def query(game, stats):
    ans = input("What statistic would you like to look at specifically?\n")
    for i in range(len(stats)-1):
        if stats[i] == ans:
            print(stats[i] + ": " + game[i])

# Display MVP's FG%, REB, AST as well
def analyze(displayed, home, away, game, homePlayers, awayPlayers, playerInfo, homeColor, awayColor, specs):
    stats = ["Date","GameID","Status","HomeID","AwayID","Season","IDHome","PTS","FG_PCT","FG3_PCT","FT_PCT","FTA","AST","REB","STL","BLK","TO"]
    statVerb = ["scored","shot","shot","made","got to the line","dished out","grabbed","stole the ball","had","had"]
    statNoun = ["points","percent from the field","percent from 3","percent of his free throws","times","assists","rebounds","times","blocks","turnovers"]
    statData = [0] * 17 
    wLData = []
    results = []
    homeMVP = [''] * 20 # contains name, pts, FGM, FGA, reb, asts, ... , home/away 
    awayMVP = [''] * 20 # ^
    reqMVP = [''] * 20 # ^
    maxHomeScore = 0 
    maxAwayScore = 0 
    # contains relevant i's of player data
    rel = [7,8,10,9,1,11,12]
    # contains relevant i's of MVP data
    MVPrel = [5,26,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,27]
    # contains i's for accessing/storing stat data
    statIndices = [16,22,23,24]
    statStoreI = [11,14,15,16]
    homeData = [0] * 17
    awayData = [0] * 17

    # void: set vars to either home or away based on who won
    def setWinner(lst, tw, tl, MVPw, maxScore, wpt, lpt):

        lst.append(tw)
        lst.append(tl)
        lst.append(wpt)
        lst.append(lpt)
        lst.append(MVPw)
        lst.append(maxScore)

    # gather home and away stat data as well as find MVP
    def storeStats(players, maxScore, MVP, data, reqMVP): 
        for x in players:
            if x[5] == reqMVP[0]:
                for i in range(0, len(reqMVP)-1):
                    reqMVP[i] = x[MVPrel[i]]
                if players == homePlayers:
                    reqMVP[-1] = "home"
                else:
                    reqMVP[-1] = "away"
            if x[26] == "": 
                maxScore += 0 
            elif int(float(x[26])) > maxScore: 
                maxScore = int(float(x[26])) 
                for i in range(0, len(MVP)):
                    MVP[i] = x[MVPrel[i]]
            for j in range(0, len(statIndices)):
                if x[statIndices[j]] != "":
                    data[statStoreI[j]] += int(float(x[statIndices[j]])) 

    # returns a sorted stat list by notability, used for both good and bad stats
    def sortStats(oldStatList, b, maxDiff, bold, unbold, reset, results):

        def last(n):
            return n[1]

        newStatList = []
        if len(oldStatList) != 0:
            newStatList = sorted(oldStatList, key=last, reverse=b)
        if abs(maxDiff) > 0:
            l = ""
            for i in range(0, len(newStatList)):
                if i <= 2:
                    if i == 0 and len(newStatList) == 1:
                        l += bold + newStatList[i][0] + reset
                    elif i == 0 and len(newStatList) == 2:
                        l += bold + newStatList[i][0] + reset + " and "
                    elif i == 0 and len(newStatList) > 2:
                        l += bold + newStatList[i][0] + reset + ", "
                    elif i == 1 and len(newStatList) > 2:
                        l += unbold + newStatList[i][0] + reset + ", and "
                    else:
                        l += unbold + newStatList[i][0] + reset
            results.append(l) 
        else:
            results.append("N/A")

        return newStatList

    # returns a array of data on notable statistic
    def evalNotable(players, playersI, madeI, attI, minAtt):
        maxNotableStat = 0
        made = 0
        attempted = 0
        notableMVP = ""

        notableList = []
        for x in players:
                if x[playersI] != "":
                    if int(float(x[attI])) > minAtt:
                        if float(x[playersI]) > maxNotableStat: 
                            maxNotableStat = float(x[playersI])
                            made = int(float(x[madeI]))
                            attempted = int(float(x[attI]))
                            notableMVP = x[5]

        # append all the locals
        notableList.append(maxNotableStat)
        notableList.append(made)
        notableList.append(attempted)
        notableList.append(notableMVP)

        return notableList

    # appends MVP data to the main results list
    def sendMVPData(req, MVP, results, lb):
        msg = ""
        lastMsg = ""
        term = [""," points (","","","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT","OREB","DREB","rebounds","assists",
        "steals","blocks","turnovers","personal fouls","plus-minus"]
        MVPdata = []
        reqOnlyData = []
        if req:
            results.append("Requested player ")
            msg = " scored "
        else:
            msg = " scored a team-high "
        # print(MVP)
        for i in range(0, len(MVP)): 
            # print(str(i) + ": " + str(MVP[i]))
            if i != 0:
                if MVP[i] != '':
                    if "in" in MVP[i]:
                        lastMsg = MVP[i]
                    elif MVP[i] != "home" and MVP[i] != "away":
                        s = float(MVP[i])
                        if s > lb or i == 4 or i == 7 or i==10 or i == 19:
                            if i == 1:
                                results.append(str(int(s)) + term[i])
                            elif i == 2:
                                results.append(str(int(s)) + "-")
                            elif i == 3:
                                results.append(str(int(s)) + ") ")
                            elif i > 12 and i < 18:
                                MVPdata.append((str(s), term[i]))
                            elif i == 4 or i == 7 or i == 10:
                                reqOnlyData.append((str(round(s,2)), term[i]))
                            else:
                                reqOnlyData.append((str(s), term[i]))
                        else:
                            results.append("N/A")
            else:
                results.append(str(MVP[i]))
                results.append(msg)

        def first(n):
            return n[0]   

        MVPdata = sorted(MVPdata, reverse=True, key=first)
        print(MVPdata)
        results.append("to go along with " + str(int(float(MVPdata[0][0]))) + " " + str(MVPdata[0][1]))
        if len(MVPdata) > 1:
            results.append(" and " + str(int(float(MVPdata[1][0]))) + " " + str(MVPdata[1][1]))
        results.append(lastMsg + ".")

    # formats row of table
    def printRow(i, s, wI, lI, color, reset, results):
        # print(f'{s[i][0]:10}' + f'{str(s[i][wI]):7}' + "| " + f'{str(s[i][lI]):7}' + "  ==>  " + color + str(s[i][3]), reset)
        results.append(f'{s[i][0]:10}' + f'{str(s[i][wI]):7}' + "| " + f'{str(s[i][lI]):7}' + "  ==>  " + color + str(s[i][3]) + reset + "\n")

    # color stat green if good (bold green if best), red if bad (bold red if worst), white if insignificant
    def printTable(g, b, wI, lI, dData, results):
        # print("Team Statistics: (W | L ==> Difference) \n")
        results.append("Team Statistics: (W | L ==> Difference) \n\n")
        for i in range(0, len(dData)):
            if dData[i][0] in g[0:3]:
                if dData[i][0] == g[0]:
                    printRow(i, dData, wI, lI, BGREEN, RESET, results)
                else:
                    printRow(i, dData, wI, lI, GREEN, RESET, results)
            elif dData[i][0] in b[0:3]:
                if dData[i][0] == b[0]:
                    printRow(i, dData, wI, lI, BRED, RESET, results)
                else:
                    printRow(i, dData, wI, lI, RED, RESET, results)
            else:
                printRow(i, dData, wI, lI, RESET, RESET, results)

    # grab stats
    for x in specs:
        if 'playerPerformance' in x:
            reqMVP[0] = x[1].split(":")[0]
    storeStats(homePlayers, maxHomeScore, homeMVP, homeData, reqMVP)
    storeStats(awayPlayers, maxAwayScore, awayMVP, awayData, reqMVP)

    # calculate stat differences
    for i in range(7,14):
        if i == 8 or i == 9 or i == 10:
            if game[rel[i-7]] != '':
                homeData[i] = round(float(game[rel[i-7]]), 2)
            if game[rel[i-7]+7] != '':
                awayData[i] = round(float(game[rel[i-7]+7]), 2)
        elif i == 11:
            statData[i] = None # skip FTA
        else:
            if game[rel[i-7]] != '':
                homeData[i] = int(float(game[rel[i-7]]))
            if game[rel[i-7]+7] != '':
                awayData[i] = int(float(game[rel[i-7]+7]))

    for i in range(7, 17):
        if i == 8 or i == 9 or i == 10:
            statData[i] = round(homeData[i] - awayData[i], 2)
        else:
            statData[i] = homeData[i] - awayData[i]
            
    if statData[7] > 0:
        setWinner(wLData, home, away, homeMVP, maxHomeScore, game[7], game[14])
        
    else:
        setWinner(wLData, away, home, awayMVP, maxAwayScore, game[14], game[7])
        
    winner = wLData[0]
    loser = wLData[1]
    winScore = wLData[2]
    loseScore = wLData[3]
    MVP = wLData[4]
    MVPscore = wLData[5]

    ptDiff = abs(statData[7])
    if ptDiff >= 20:
        winMsg = "blew out"
    elif ptDiff >= 10:
        winMsg = "defeated"
    elif ptDiff >= 2:
        winMsg = "beat"
    else:
        winMsg = "just barely survived"
  
    if winner == away: # invert every stat difference if away team won
        for i in range(7,17):
            if statData[i] != 0:
                statData[i] *= -1
 
    goodStats = [] # list of tuples: ("Stat Category", Value)
    badStats = [] # ^
    maxDiff = 0
    maxDiffStat = ""
    minDiff = 0
    minDiffStat = ""
    tempStatData = [0] * 17

    # copy statData to make calculations
    for i in range(0, len(statData)):
        tempStatData[i] = statData[i] 

    # find maxDiff and minDiff statistics
    statWeights = [0,0,0,0,0,0,0,1,100,100,100,1,1,1,1,1,-1]
    for i in range(8,17): 
        tempStatData[i] *= statWeights[i]
        if tempStatData[i] > 4:
            goodStats.append(((stats[i]), tempStatData[i]))
            if tempStatData[i] > maxDiff:
                maxDiff = tempStatData[i]
                maxDiffStat = stats[i]
        if tempStatData[i] < -5:
            badStats.append(((stats[i]), tempStatData[i]))
            if statData[i] < minDiff:
                minDiff = tempStatData[i]
                minDiffStat = stats[i]

    goodStatsReported = []
    badStatsReported = []
    revGoodStats = sortStats(goodStats, True, maxDiff, BGREEN, GREEN, RESET, goodStatsReported)
    revBadStats = sortStats(badStats, False, minDiff, BRED, RED, RESET, badStatsReported)

    if displayed:

        winnerColor = ""
        loserColor = ""

        if winner == home:
            winnerColor = homeColor
            loserColor = awayColor
        else:
            winnerColor = awayColor
            loserColor = homeColor

        # create parallel arrays with just the names
        goodStatNames = []
        badStatNames = []
        for i in range(0,len(revGoodStats)): 
            goodStatNames.append(revGoodStats[i][0])
        for i in range(0,len(revBadStats)): 
            badStatNames.append(revBadStats[i][0])

        # determine index of most notable stat in stats[]
        statI = 0
        if len(goodStatNames) != 0:
            for i in range(0, len(stats)):
                if goodStatNames[0] == stats[i]:
                    statI = i-7
                    break

        # determine index of most notable stat in playerInfo[]
        playersI = 0
        if len(goodStatNames) != 0:
            for i in range(0, len(playerInfo)):
                if goodStatNames[0] == playerInfo[i]:
                    playersI = i
                    break

        # find index of notable statistic
        madeI = 0
        attI = 0
        minAtt = 0
        if playersI == 11 or playersI == 14 or playersI == 16 or playersI == 17:
            if playersI == 16:
                attI = playersI
                minAtt = 5 # FTA
            elif playersI == 17:
                attI = playersI - 1
                minAtt = 4 # FG3A
            else:
                attI = playersI - 1
                minAtt = 5 # FGA
            madeI = attI - 1

        notableData = []
        if home == winner:
            if reqMVP[6] == "home":
                reqMVP[6] = " in the " + GREEN + "win" + RESET
            else:
                reqMVP[6] = " in the " + RED + "loss" + RESET
            if statI != 9:
                notableData = evalNotable(homePlayers, playersI, madeI, attI, minAtt)
            else:
                notableData = evalNotable(awayPlayers, playersI, madeI, attI, minAtt)
        else:
            if reqMVP[6] == "away":
                reqMVP[6] = " in the " + GREEN + "win" + RESET
            else:
                reqMVP[6] = " in the " + RED + "loss" + RESET
            if statI != 9:
                notableData = evalNotable(awayPlayers, playersI, madeI, attI, minAtt)
            else:
                notableData = evalNotable(homePlayers, playersI, madeI, attI, minAtt)

        maxNotableStat = notableData[0]
        made = notableData[1]
        attempted = notableData[2]
        notableMVP = notableData[3]
        keyPlayer = []

        if maxNotableStat == 0 or maxNotableStat > 100:
            keyPlayer.append("N/A")
        elif playersI == 11 or playersI == 14 or playersI == 16 or playersI == 17:
            if playersI != 16:
                maxNotableStat = round(maxNotableStat*100,2)
            else:
                maxNotableStat = int(maxNotableStat)
            keyPlayer.append(notableMVP + " " + statVerb[statI] + " " + str(maxNotableStat) + " " + 
            str(statNoun[statI]) + f' ({made}-{attempted}), which heavily impacted the game.\n')
        else:
            maxNotableStat = int(maxNotableStat)
            keyPlayer.append(notableMVP + " " + statVerb[statI] + " " + str(maxNotableStat) + " " + 
            str(statNoun[statI]) + ", which heavily impacted the game.\n")        
        
        # send winner MVP first, then loser MVP
        winMVP = []
        loseMVP = []

        MVP.append(" in the " + GREEN + "win" + RESET)
        sendMVPData(False, MVP, winMVP, 1)
        if MVP == homeMVP:
            awayMVP.append(" in the " + RED + "loss" + RESET)
            sendMVPData(False, awayMVP, loseMVP, 1)
        else:
            homeMVP.append(" in the " + RED + "loss" + RESET)
            sendMVPData(False, homeMVP, loseMVP, 1)

        # if requested player, send statline
        reqMVPDis = []
        if reqMVP[1] != '' and reqMVP[0] != homeMVP[0] and reqMVP[0] != awayMVP[0]:
            sendMVPData(True, reqMVP, reqMVPDis, -1)
        else:
            reqMVPDis.append('N/A')

        # multiply percentages by 100 for readability
        for i in range(8, 11):
            homeData[i] = round(homeData[i]*100, 2)
            awayData[i] = round(awayData[i]*100, 2)
            statData[i] = round(statData[i]*100, 2)

        # make this into a function
        if len(goodStatNames) < 3:
            if len(goodStatNames) < 1:
                goodStatNames.append("")
            if len(goodStatNames) < 2:
                goodStatNames.append("")
            goodStatNames.append("")

        if len(badStatNames) < 3:
            if len(badStatNames) < 1:
                badStatNames.append("")
            if len(badStatNames) < 2:
                badStatNames.append("")
            badStatNames.append("")

        def last(n):
                return n[3]

        # invert turnover number
        statData[16] *= -1

        fullStatData = []
        for i in range(8, len(stats)):
            fullStatData.append([stats[i], homeData[i], awayData[i], statData[i]])
        ordStatData = sorted(fullStatData, key=last, reverse=True)

        results.append("\nW: " + "\033[1;38;5;" + winnerColor + winner + RESET + ", " + "L: " + 
        "\033[1;38;5;" + loserColor + loser + RESET + "\n\n")

        # print out score before printing table
        if winner == home:
            results.append("Score:   " + str(homeData[7]) + "  -  " + str(awayData[7]) + RESET + "\n\n")
            printTable(goodStatNames, badStatNames, 1, 2, ordStatData, results)
        else:
            results.append("Score:   " + str(awayData[7]) + "  -  " + str(homeData[7]) + RESET + "\n\n")
            printTable(goodStatNames, badStatNames, 2, 1, ordStatData, results)

        # sum of stat differences correlates with competitiveness
        compScore = int(sum(statData[7:]))
        compSpec = ['*'] * 10
        results.append("\nSum of Stat Differences: ==>  " + CYAN + str(compScore) + RESET + "\n\n")

        # if compScore is negative, set to 0
        if compScore < 0:
            compScore = 0

        # if compScore is 60 or above, set to 60
        if compScore > 59:
            compScore = 60

        # rescale sum of stat differences to fit on spectrum
        compScore = int((round(compScore*1.5/10)*10)/10)

        # print out spectrum, color compScore index cyan
        results.append("Very Competitive | ")
        for i in range(0, len(compSpec)):
            if i == compScore:
                compSpec[i] = CYAN + compSpec[i] + RESET
            results.append(compSpec[i] + " ")
        results.append("| Not Very Competitive\n\n")

    # NON-DIS CARES ABOUT
    results.append(winner + " ") 
    results.append(winMsg + " the ")
    results.append(loser + " ") 
    if winScore != '':
        results.append(str(int(float(winScore))) + " to ") 
    if loseScore != '':
        results.append(str(int(float(loseScore)))) 
    if "N/A" not in goodStatsReported:
        results.append(" thanks to better " + goodStatsReported[0])
    if "N/A" not in badStatsReported:
        results.append(" despite worse " + badStatsReported[0] + ".\n\n")
    else:
        results.append(".\n\n")

    if displayed:
        if keyPlayer[0] != "N/A":
            results.append(keyPlayer[0] + "\n")
        for x in winMVP:
            if x != "N/A":
                results.append(x)
        results.append("\n\n")
        for y in loseMVP:
            if y != "N/A":
                results.append(y)
        results.append("\n\n")
        pickedPlayer = ""
        for z in reqMVPDis:
            if z != "N/A":
                results.append(z)
                pickedPlayer = "\n\n"
        results.append(pickedPlayer)
        results.append(game[len(game)-1])
    else:
        results.append(homeColor)
        results.append(awayColor)

    return(results)

    # END OF ANALYZE--------------------------------------------------------------------------------------

def printSeparator():
    # print separator line
    separator = ['-'] * 100
    for j in range(0, len(separator)):
        print(separator[j], end="")
    print()
    
def welcome(gameData, attributes, teamData, gameDetails, playerInfo, playerData):
    ### TODO ###
    # SPLIT UP DISPLAY FUNC
    # change year to season
    # team1, team2 (instead of home_team, away_team)
    # don't pick randomly from final gameList, iterate through (pass i to newSearch), or random no rep
    # add category 'performance'
    # e.g. "Marcus Smart", "TO<5", "win" (optional param), use sets!
    # reject invalid team name
    # get below 800 lines
    # speed up winReason (use sets)
    # display team's record for that season
    # be able to look for games that contain more than one player (differentiate teammates vs. matchups)
    # calculate player or team avg. of a statistic, either all-time or season-based
    # display stats such as BLK and STL if they are higher than either REB or AST
    # look for games with triple-double scorers
    # CONDENSE EVERYTHING!!!!

    ### IDEAS FOR USE ###
    # tell a team where its strengths and weaknesses are (winReason)
    # tell a team for what reason (statistically) they lose to a specific opponent (also winReason)
    # tell a team when a player helps/harms them (performance)

    #### DISPLAY #### -- display analysis of game ----------------------------------------------------
    def display(displayed, gameList, gameI, gameData, teamData, gameDetails, playerInfo, stat, name, specs):

        # replay prompt to analyze a new game ---------------------------------------------------------
        def newSearch(msg, s, n, specs):
            replay = ""
            prompt = msg + "Would you like to analyze another "
            for x in specs:
                prompt += str(x[0]) + "=" + str(x[1])
                if x != specs[len(specs)-1]:
                    prompt += ", "
            if prompt == msg + "Would you like to analyze another ":
                prompt += "random"
            if s == "random":
                replay = input(prompt + " game? (y or n)\n\n")
                if replay == 'y': 
                    newGameI = random.randint(0, len(gameData)-1)
                    print()
                    display(True, gameList, newGameI, gameData, teamData, gameDetails, playerInfo, stat, name, specs)
                elif replay == 'n':
                    print()
                    welcome(gameData, attributes, teamData, gameDetails, playerInfo, playerData)
                else:
                    print()
                    newSearch("I'm sorry, I didn't quite get that. ", s ,n, specs)
            else:
                replay = input(prompt + " game? (y or n)\n\n")
                if replay == 'y': 
                    if len(gameList) > 1:
                        ind = random.randint(0, len(gameList)-1)
                        newGameI = gameList[ind]
                    elif len(gameList) == 1:
                        newGameI = gameList[0]
                    else:
                        newGameI = random.randint(0, len(gameData)-1)
                    print()
                    display(True, gameList, newGameI, gameData, teamData, gameDetails, playerInfo, stat, name, specs)
                elif replay == 'n': 
                    print()
                    welcome(gameData, attributes, teamData, gameDetails, playerInfo, playerData)
                else:
                    print()
                    newSearch("I'm sorry, I didn't quite get that. ", s ,n, specs)
        
        pickedGame = gameI
        game = gameData[pickedGame]
        homePlayers = []
        awayPlayers = []
        teams = []
        teamColors = ['45m','106m','160m','88m','34m','203m','86m','9m','198m','87m','148m','98m','202m','129m','33m',
        '27m','153m','220m','226m','216m','198m','1m','196m','245m','214m','166m','46m','124m','221m','69m']
        home = ""
        away = ""

        # classify the home and away team
        for x in teamData:
            teams.append(x[5])
            if x[1] == game[3]:
                home = x[5]
            elif x[1] == game[4]:
                away = x[5]
        
        # store home and away players in their respective list
        for x in gameDetails:
            if x[0] == game[1]:
                if x[1] == game[3]:
                    homePlayers.append(x)
                elif x[1] == game[4]:
                    awayPlayers.append(x)

        # default home and away color
        homeColor = '\033[1;38;5;202m'
        awayColor = '\033[1;38;5;198m'

        sortedTeams = sorted(teams)
        homeColor = teamColors[sortedTeams.index(home)]
        awayColor = teamColors[sortedTeams.index(away)]

        # check if playoff or finals matchup
        playoff = " "
        playoffMonths = ["04","05"]
        bubblePlayoffMonths = ["08","09"]
        years = ["2003","2004","2005","2006","2007","2008","2009","2010",
        "2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021"]
        playoffStartDates = [18, 16, 22, 22, 20, 19, 17, 16, 15, 27, 19, 18, 17, 15, 14, 13, 12, 16, 21]
        finalStartDates = [3, 5, 8, 7, 6, 4, 3, 2, 0, 11, 5, 4, 3, 1, 0, 0, 0, 0, 0]
        gameYear = gameData[pickedGame][0].split("-")[0]
        gameMonth = gameData[pickedGame][0].split("-")[1]
        gameDay = gameData[pickedGame][0].split("-")[2]

        # CONDENSE THIS
        if gameYear == "2020":
            if gameMonth in bubblePlayoffMonths:
                if gameMonth == "09" and gameDay == "30":
                    playoff = " finals "
                elif gameMonth == "08":
                    if int(gameDay) > playoffStartDates[years.index(gameYear)]:
                        playoff = " playoff "
                else:
                    playoff = " playoff "
            elif gameMonth == "10":
                playoff = " finals "

        if gameMonth in playoffMonths:
            if gameMonth == "04":
                if int(gameDay) > playoffStartDates[years.index(gameYear)]:
                    playoff = " playoff "
            else:
                playoff = " playoff "
        elif gameMonth == "06":
            if int(gameDay) > finalStartDates[years.index(gameYear)]:
                playoff = " finals "
            else:
                playoff = " playoff "

        results = []
        if displayed:
            print("Today we'll be looking at " + BOLDW + game[0] + RESET + "'s " + '\033[1;38;5;' + homeColor + home + RESET + " vs. " + '\033[1;38;5;' + awayColor + away + RESET + BOLDW + playoff + RESET + "matchup.\n", RESET) 
            q = "Do you want to analyze? (y or n or quit) \n\n" 
            # recursive loop where user can decide whether or not to analyze
            def studyGame(ques):
                inp = input(ques)
                if inp == "y":
                    print() 
                    print("***** Analyzing ***** ")
                    results = analyze(displayed, home, away, game, homePlayers, awayPlayers, playerInfo, homeColor, awayColor, specs)
                    for x in results:
                        if x != results[len(results)-1]:
                            print(str(x), end="")
                    newSearch("", stat, name, specs)
                elif inp == "n":
                    print()
                    welcome(gameData, attributes, teamData, gameDetails, playerInfo, playerData)
                elif inp == "quit":
                    print("\nQuitting...\n")
                else:
                    print("\nI'm sorry, I didn't quite get that.\n")
                    studyGame(ques)
                    
            studyGame(q)
        else:
            results = analyze(displayed, home, away, game, homePlayers, awayPlayers, playerInfo, homeColor, awayColor, specs)
            results.append(home)
            results.append(away)
            results.append(game[0])
            return results

    # recursive function that prompts possible search parameters until 'go' is entered
    def completeSearch(ans):
        inpString = "Select a category to narrow your search. When finished, enter \'" + BGREEN + "go" + RESET + "'.\n\n"
        for i in range(0, len(searchOptions)-1):
            if catList[i] != "?":
                inpString += str(searchOptions[i]) + "=" + YELLOW + str(catList[i]) + RESET + ", "
            else:
                inpString += str(searchOptions[i]) + "=" + str(catList[i]) + ", "
        inpString += str(searchOptions[len(searchOptions)-1]) + "\n\n"
        if ans != 'go': 
            ans3 = input(inpString)
            if ans3 in searchOptions: 
                ans2 = input("\nWhich " + ans3 + " would you like to select?\n\n")
                print()
                if ans3 == 'month': 
                    if ans2 in monthNames:
                        catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                        ans2 = monthNums[monthNames.index(ans2)]
                        if len(specs) != 0 and ans3 == ans and ans3 not in catList and ans in monthNames:
                            specs.remove(specs[len(specs)-1])
                        specs.append((ans3, ans2)) 
                        completeSearch(ans3) 
                    else:
                        print("That's not a valid month.\n")
                        completeSearch(ans3) 
                else:
                    # correct an already entered param
                    if len(specs) != 0 and ans3 == ans and ans3 not in catList:
                        specs.remove(specs[-1])
                    # don't append special categories
                    if ans3 != "winReason" and ans3 != "playerPerformance":
                        specs.append((ans3, ans2)) 
                    elif ans3 == "playerPerformance":
                        # perf = [True, ans2.split(":")[0], ans2.split(":")[1]]
                        specs.append((ans3, ans2))
                    else:
                        if ":" in ans2:
                            wReason[0] = (True, ans2.split(":")[0], ans2.split(":")[1])
                        else:
                            print("Please answer using the format \"home/away:stat\".\n")
                            completeSearch(ans3)
                    catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                    completeSearch(ans3) 
            elif ans3 != 'go':
                if ans3 == "random":
                    print("\nChoosing random game...\n")
                    ans2 = "random"
                    pickedGame = random.randint(0, len(gameData)-1)
                    completeSearch("go")
                else:
                    print("\nI'm sorry, I didn't quite get that.\n") 
                    completeSearch(ans3)
            else:
                print()
                completeSearch(ans3)
        else:
            return 
    
    # create set of all player performances, keep those that meet criteria
    def createPlayerSet(on):
        gameDetSet = {"1"}
        if playerParam:
            for i in range(0, len(gameDetails)):
                addString = ""
                if gameDetails[i][8] != "":
                    addString += gameDetails[i][0]
                    if perfData[0] == "any":
                        addString += ":any:"
                    else:
                        addString += ":" + gameDetails[i][5] + ":"
                    if ">" in perfData[1]:
                        pStat = perfData[1].split(">")[0]
                        statVal = perfData[1].split(">")[1]
                        if gameDetails[i][playerInfo.index(pStat)] != "":
                            if float(gameDetails[i][playerInfo.index(pStat)]) > float(statVal):
                                # print(float(gameDetails[i][playerInfo.index(pStat)]))
                                addString += perfData[1]
                    elif "<" in perfData[1]:
                        pStat = perfData[1].split("<")[0]
                        statVal = perfData[1].split("<")[1]
                        if gameDetails[i][playerInfo.index(pStat)] != "":
                            if float(gameDetails[i][playerInfo.index(pStat)]) < float(statVal):
                                # print(float(gameDetails[i][playerInfo.index(pStat)]))
                                addString += perfData[1] 
                    else:
                        addString += "any"

                gameDetSet.add(addString + ":")

        gameDetSet.remove("1")

        return gameDetSet

    # if reason, keep home/away games won by reason
    def checkReason(reasonData, color, i):
        reasonUsed = reasonData[0][0]
        side = reasonData[0][1]
        stat = reasonData[0][2]
        coll = []
        preSort = []
        removedGames = []
        if reasonUsed: 
            for x in gameList:
                keep = False
                winner = ""
                loser = ""
                if len(gameList) == 0:
                    break
                coll.append(display(False, gameList, x, gameData, teamData, gameDetails, playerInfo, ans1, ans2, specs)) 
                if stat != "any":
                    statReason = color + stat 
                else:
                    statReason = ","
                # keep = true if home selected and won
                if str(coll[-1][-3]) + " " == coll[-1][0] and side == "home": 
                    keep = True
                # keep = true if away selected and won
                if str(coll[-1][-2]) + " " == coll[-1][0] and side == "away": 
                    keep = True
                if side == "any":
                    keep = True
                if statReason not in coll[-1][i] or not keep:
                    removedGames.append(x)

        for y in removedGames:
            gameList.remove(y)

    ##### WELCOME #####

    # data for search and welcome screen
    searchOptions = ["year","month","day","home_team","away_team","winReason","playerPerformance","random game"]
    # display version of searchOptions
    searchOpDis = ["year","month","day","home_team","away_team","winReason","playerPerformance","random game"]
    catList = ["?","?","?","?","?","?","?","?","?"]
    searchI = [0,0,0,3,4,1,1]
    monthNames = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    monthNums = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    specs = [] # holds tuple responses to searchOptions, (category, response)
    gameList = []
    pickedGame = 0
    reqPlayer = "N/A"
    wReason = [(False,"","")]
    perf = [False,"",""]

    print(YELLOW + "Welcome to NBA Researcher!\n", RESET)
    completeSearch("") # fills specs[]
    ans1 = ""
    ans2 = ""
    print("Searching...\n")

    # if playerPerformance in specs, parse
    perfData = []
    playerParam = False
    for x in specs:
        if "playerPerformance" in x:
            perfData = x[1].split(":")
            playerParam = True

    # create set of all player performances
    print("Creating player set...")
    pSet = createPlayerSet(playerParam)

    # does game(i) contain all of the specifications?
    for i in range(0, len(gameData)):
        # holds specified aspect of game(i)
        x = ""
        checkList = []
        for j in range(0, len(specs)): 
            x = gameData[i][searchI[searchOptions.index(specs[j][0])]]
            if specs[j][0] == "year" or specs[j][0] == "month" or specs[j][0] == "day":
                x = x.split("-")[searchOptions.index(specs[j][0])]
            elif specs[j][0] == "home_team" or specs[j][0] == "away_team":
                for k in range(0, len(teamData)):
                    if teamData[k][1] == x:
                        x = teamData[k][5]
            else:
                x = str(x) + ":" + specs[j][1] + ":"
                # print(x)
                if x in pSet:
                    x = specs[j][1]

            if x == specs[j][1]:
                checkList.append(specs[j]) 
        if checkList == specs:
            gameList.append(i) # index of gameData is appended

    checkReason(wReason, BGREEN, 5)
    validGame = []
    resultList = []
    winCol = ""
    loseCol = ""
    print("\nDisplaying results...\n")
    for x in gameList:
        validGame = display(False, gameList, x, gameData, teamData, gameDetails, playerInfo, ans1, ans2, specs)
        if str(validGame[-3]) + " " == validGame[0]:
            winCol = validGame[-5]
            loseCol = validGame[-4]
        if str(validGame[-2]) + " " == validGame[0]: 
            winCol = validGame[-4]
            loseCol = validGame[-5]
        resultList.append(gameData[x][0] + " W: \033[1;38;5;" + winCol + validGame[0] + RESET + "L: \033[1;38;5;" + loseCol + validGame[2] + RESET)
    finalResultList = sorted(resultList, reverse=True)
    for x in finalResultList:
        print(x)
    if len(gameList) != 0:
        r = random.randint(0, len(gameList)-1)
        print("\n" + str(len(gameList)) + " games found!\n")
        pickedGame = gameList[r]
    else:
        pickedGame = random.randint(0, len(gameData)-1)
        print("Sorry, no games found. Picking random game:\n")
        specs.clear()
        ans2 = "random"

    # display analysis of picked game
    if wReason[0][0]:
        specs.append(("winReason", wReason[0][1] + ":" + wReason[0][2]))
    display(True, gameList, pickedGame, gameData, teamData, gameDetails, playerInfo, ans1, ans2, specs)

def main():
    print(RED + "Reading in game database...\n", RESET)
    folder = sys.argv[1]
    gameData = read_csv(folder + "/games.csv")
    attributes = gameData[0]
    teamData = read_csv(folder + "/teams.csv")
    gameDetails = read_csv(folder + "/games_details.csv")
    playerData = read_csv(folder + "/players.csv")
    gameData.pop(0)
    teamData.pop(0)
    playerInfo = gameDetails[0]
    gameDetails.pop(0)
    playerData.pop(0)
    welcome(gameData, attributes, teamData, gameDetails, playerInfo, playerData)
   
if __name__ == '__main__':
    main()
