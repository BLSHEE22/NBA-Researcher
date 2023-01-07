### TODO ###
    # playoff games on the game table should be a different color
    # add more color encoding to the statistical report
    # ptpr should be able to track multiple statlines
    # have "performance" part of PTPR handle equations. And perhaps relations to other players!
    # Add "huck" index, where a player's FGA can get too high where it yields a losing % > career losing %
    # - minimum # of games per FGA# must be 10% of player's total career games
    # Add "rivalry" heuristic, measures competitiveness of matchups
    # Ask if the user wants to AMEND their search or start a new one
    # >>>>>>> redisplay gameList after first analysis
    # SPLIT UP DISPLAY FUNC
    # PROVE implications: e.g., Marcus Smart:FGA>14 => L (calculate percent chance)
    # 'prove' category
    # change year to season
    # get below 800 lines (hahahaha)
    # speed up winReason (use sets)
    # display team's record for that season
    # be able to look for games that contain more than one player (differentiate teammates vs. matchups)
    # calculate player or team avg. of a statistic, either all-time or season-based
    # look for games with triple-double scorers
    # CONDENSE EVERYTHING!!!!

    ### IDEAS FOR USE ###
    # tell a team where its strengths and weaknesses are (winReason)
    # tell a team for what reason (statistically) they lose to a specific opponent (also winReason)
    # tell a team when a player helps/harms them (performance)

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

# format blurb for a game based on its box score
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
    MVPrel = [5,27,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28] # added 1 after 5
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
            #print(homeMVP)
            #print(awayMVP)
            if x[5] == reqMVP[0]:
                for i in range(0, len(reqMVP)-1):
                    reqMVP[i] = x[MVPrel[i]]
                if players == homePlayers:
                    reqMVP[-1] = "home"
                else:
                    reqMVP[-1] = "away"
            # check if player has the maxScore
            if x[27] == "": 
                maxScore += 0 
            elif int(float(x[27])) > maxScore: 
                maxScore = int(float(x[27])) 
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
    def sendMVPData(req, MVP, results, lb, reqStat, alreadyMVP, reqStatNews):
        #if(req):
            #print("MVP: " + str(MVP))
            #print("results: " + str(results))
            #print("lb: " + str(lb))
        msg = ""
        lastMsg = ""
        term = [""," points (","","","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT","OREB","DREB","rebounds","assists",
        "steals","blocks","turnovers","personal fouls","plus-minus"]
        termTrans = ["Name","PTS","FGM","FGA","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT","OREB","DREB","REB","AST",
        "STL","BLK","TO","PF","+/-"]
        reqStatV = ["was","scored","made","attempted","shot","made","attempted","shot","made","attempted","shot","grabbed","grabbed",
                    "grabbed","dished out","had","had","had","had","had a"]
        reqStatN = ["himself","points","shots from the field","shots from the field","percent from the field","threes","threes","percent from three",
                    "free throws","free throws","percent from the line","offensive rebounds","defensive rebounds","rebounds","assists","steals",
                    "blocks","turnovers","personal fouls","plus/minus"]
        MVPdata = []
        reqOnlyData = []
        req1 = True
        req2 = True
        intFloat = 0
        #print(MVP)
        if req:
            if reqStat != "":
                if reqStat == "FG_PCT" or reqStat == "FG3_PCT" or reqStat == "FT_PCT":
                    intFloat = str(float(MVP[termTrans.index(reqStat)])*100)
                else:
                    intFloat = str(int(float(MVP[termTrans.index(reqStat)])))
                results.append("This game fit the criteria as " + str(MVP[0]) + " " 
                                + reqStatV[termTrans.index(reqStat)] + " " + BOLDW
                                + intFloat + RESET + " " + reqStatN[termTrans.index(reqStat)])
                if not alreadyMVP:
                    results.append(".\n\nHis main statline ")
                    MVP[0] = "was "
            elif not alreadyMVP:
                results.append("Requested player ")
                msg = " scored "
            else:
                msg += ""
                req1 = False
        if not alreadyMVP:
            for i in range(0, len(MVP)): 
                if not req and i == 0:
                    msg += " scored a team-high "
                if i != 0:
                    if MVP[i] != '':
                        if "in" in MVP[i]:
                            lastMsg = MVP[i]
                        elif MVP[i] != "home" and MVP[i] != "away":
                            s = float(MVP[i])
                            if s > lb or i == 4 or i == 7 or i == 10 or i == 19:
                                if i == 1:
                                    results.append(str(int(s)) + term[i])
                                elif i == 2:
                                    results.append(str(int(s)) + "-")
                                elif i == 3:
                                    results.append(str(int(s)) + ") ")
                                elif i == 4 or i == 7 or i == 10:
                                    reqOnlyData.append((100*round(s,2), term[i]))
                                elif i == 5:
                                    MVP.append((int(s), term[i]))
                                elif i > 12 and i < 18:
                                    MVPdata.append((int(s), term[i]))
                                else:
                                    reqOnlyData.append((s, term[i]))
                            else:
                                results.append("N/A")
                else:
                    results.append(str(MVP[i]))
                    results.append(msg)
        else:
            req2 = False

        def first(n):
            return n[0]   

        MVPdata = sorted(MVPdata, reverse=True, key=first)
        # print("MVPdata: " + str(MVPdata))
        if len(MVPdata) > 0:
            results.append("to go along with " + str(int(float(MVPdata[0][0]))) + " " + str(MVPdata[0][1]))
        if len(MVPdata) > 1:
            results.append(" and " + str(int(float(MVPdata[1][0]))) + " " + str(MVPdata[1][1]))
        if req1 or req2:
            results.append(lastMsg + ".")
        else:
            lastMsg = ""
        # print(results)

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

    reqMVPStat = ""

    # grab stats
    for x in specs:
        if 'ptpr' in x:
            reqMVP[0] = x[1].split(":")[0]
            perf = x[1].split(":")[2]
            if ">" in perf: 
                reqMVPStat = x[1].split(":")[2].split(">")[0]
            elif "<" in perf: 
                reqMVPStat = x[1].split(":")[2].split("<")[0]
    # print(reqMVP)
    # print(reqMVPStat)
    storeStats(homePlayers, maxHomeScore, homeMVP, homeData, reqMVP)
    storeStats(awayPlayers, maxAwayScore, awayMVP, awayData, reqMVP)

    # calculate stat differences
    for i in range(7,14):
        # FG_PCT, FG3_PCT, or FT_PCT
        if i == 8 or i == 9 or i == 10:
            if game[rel[i-7]] != '':
                homeData[i] = round(float(game[rel[i-7]]), 2)
            if game[rel[i-7]+7] != '':
                awayData[i] = round(float(game[rel[i-7]+7]), 2)
        # skip FTA
        elif i == 11:
            statData[i] = None
        else:
            if game[rel[i-7]] != '':
                homeData[i] = int(float(game[rel[i-7]]))
            if game[rel[i-7]+7] != '':
                awayData[i] = int(float(game[rel[i-7]+7]))

    for i in range(7, 17):
        # round percentage stats
        if i == 8 or i == 9 or i == 10:
            statData[i] = round(homeData[i] - awayData[i], 2)
        else:
            statData[i] = homeData[i] - awayData[i]
    
    # print(statData)
            
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
        floatStats = [11,12,14,15,16,17,18]
        # FGM,FG_PCT,FGA,FG3_PCT,FTA,FG3A,FT_PCT
        if playersI in floatStats:
            if playersI == 16:
                attI = playersI
                minAtt = 5 # FTA
            elif playersI == 17:
                attI = playersI - 1
                minAtt = 4 # FG3A
            else:
                attI = playersI - 1
                minAtt = 5 # FGM,FG_PCT,FGA,FG3_PCT,FT_PCT
            madeI = attI - 1

        notableData = []
        if home == winner:
            if reqMVP[-1] == "home":
                reqMVP[-1] = " in the " + GREEN + "win" + RESET
            else:
                reqMVP[-1] = " in the " + RED + "loss" + RESET
            if statI != 9:
                notableData = evalNotable(homePlayers, playersI, madeI, attI, minAtt)
            else:
                notableData = evalNotable(awayPlayers, playersI, madeI, attI, minAtt)
        else:
            if reqMVP[-1] == "away":
                reqMVP[-1] = " in the " + GREEN + "win" + RESET
            else:
                reqMVP[-1] = " in the " + RED + "loss" + RESET
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
        elif playersI == 12 or playersI == 15 or playersI == 16 or playersI == 18:
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
        alreadyMVP = False
        reqStatNews = True

        MVP.append(" in the " + GREEN + "win" + RESET)
        sendMVPData(False, MVP, winMVP, 1, reqMVPStat, False, True)
        if MVP == homeMVP:
            awayMVP.append(" in the " + RED + "loss" + RESET)
            sendMVPData(False, awayMVP, loseMVP, 1, reqMVPStat, False, True)
        else:
            homeMVP.append(" in the " + RED + "loss" + RESET)
            sendMVPData(False, homeMVP, loseMVP, 1, reqMVPStat, False, True)

        # if requested player, send statline
        reqMVPDis = []
        reqUsed = False
        if reqMVP[1] != '':
            if reqMVP[0] == homeMVP[0]:
                alreadyMVP = True
            elif reqMVP[0] == awayMVP[0]:
                alreadyMVP = True
            sendMVPData(True, reqMVP, reqMVPDis, -1, reqMVPStat, alreadyMVP, reqStatNews)
        else:
            reqMVPDis.append('N/A')
        
        # print(results)

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

        results.append("\n" + game[0] + " W: " + "\033[1;38;5;" + winnerColor + winner + RESET + ", " + "L: " + 
        "\033[1;38;5;" + loserColor + loser + RESET + "\n\n")

        # print out score before printing table
        if winner == home:
            results.append("Score:     " + str(homeData[7]) + "  -  " + str(awayData[7]) + RESET + "\n\n")
            printTable(goodStatNames, badStatNames, 1, 2, ordStatData, results)
        else:
            results.append("Score:     " + str(awayData[7]) + "  -  " + str(homeData[7]) + RESET + "\n\n")
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

    # print(results)
    return(results)

    # END OF ANALYZE--------------------------------------------------------------------------------------

# prints a separator line
def printSeparator():
    # print separator line
    separator = ['-'] * 100
    for j in range(0, len(separator)):
        print(separator[j], end="")
    print()
    
# main UI and search filter - contains display() which utilizes analyze()
def welcome(gameData, attributes, teamData, gameDetails, playerInfo, playerData):

    #### DISPLAY #### -- display analysis of game ----------------------------------------------------
    def display(displayed, gameList, gameI, gameData, teamData, gameDetails, playerInfo, stat, name, specs, q):

        # replay prompt to analyze a new game ---------------------------------------------------------
        def newSearch(msg, s, n, specs):
            replay = ""
            prompt = msg + YELLOW + "Would you like to analyze another "
            for x in specs:
                prompt += str(x[0]) + "=" + str(x[1])
                if x != specs[len(specs)-1]:
                    prompt += ", "
            if prompt == msg + YELLOW + "Would you like to analyze another ":
                prompt += "random"
            if s == "random":
                replay = input(prompt + " game? (y or n or quit)\n\n" + RESET)
                if replay.lower() == 'y': 
                    newGameI = random.randint(0, len(gameData)-1)
                    print()
                    display(True, gameList, newGameI, gameData, teamData, gameDetails, playerInfo, stat, name, specs, "")
                elif replay.lower() == 'n':
                    print()
                    welcome(gameData, attributes, teamData, gameDetails, playerInfo, playerData)
                elif replay.lower() == 'quit':
                    print("\nQuitting...\n")
                    quit()
                else:
                    print()
                    newSearch(YELLOW + "I'm sorry, I didn't quite get that. " + RESET, s ,n, specs)
            else:
                replay = input(prompt + " game? (y or n or quit)\n\n" + RESET)
                if replay.lower() == 'y': 
                    if len(gameList) > 1:
                        for i in range(len(gameList)):
                            if gameList[i] == pickedGame:
                                if i == len(gameList)-1:
                                    ind = 0
                                else:
                                    ind = i + 1
                        # ind = random.randint(0, len(gameList)-1)
                        newGameI = gameList[ind]
                    elif len(gameList) == 1:
                        newGameI = gameList[0]
                    else:
                        newGameI = random.randint(0, len(gameData)-1)
                    print()
                    display(True, gameList, newGameI, gameData, teamData, gameDetails, playerInfo, stat, name, specs, "y")
                elif replay.lower() == 'n': 
                    print()
                    welcome(gameData, attributes, teamData, gameDetails, playerInfo, playerData)
                elif replay.lower() == "quit":
                    print("\nQuitting...\n")
                    quit()
                else:
                    print()
                    newSearch(YELLOW + "I'm sorry, I didn't quite get that. " + RESET, s ,n, specs)
        
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
        for i in range(len(teamData)): # -4 ????
            teams.append(teamData[i][5])
            if teamData[i][1] == game[3]:
                home = teamData[i][5]
            elif teamData[i][1] == game[4]:
                away = teamData[i][5]
        
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
            # recursive loop where user can decide whether or not to analyze
            def studyGame(ques):
                inp = ques
                if inp == "y":
                    print() 
                    print("********************* Analyzing ********************* ")
                    results = analyze(displayed, home, away, game, homePlayers, awayPlayers, playerInfo, homeColor, awayColor, specs)
                    for x in results:
                        if x != results[len(results)-1]:
                            print(str(x), end="")
                    newSearch("", stat, name, specs)
                elif inp == "n":
                    print()
                    welcome(gameData, attributes, teamData, gameDetails, playerInfo, playerData)
                elif inp == "quit":
                    print("\nQuitting... \n")
                else:
                    print("\n" + YELLOW + "I'm sorry, I didn't quite get that.\n" + RESET)
                    studyGame(ques)

            if q == "y" or q == "n":
                studyGame(q)
            else:
                print("Let's look specifically at " + BOLDW + game[0] + RESET + "'s " + '\033[1;38;5;' + homeColor + home + RESET + " vs. " + '\033[1;38;5;' + awayColor + away + RESET + BOLDW + playoff + RESET + "matchup.\n", RESET) 
                a = input("Do you want to analyze? (y or n or quit) \n\n")        
                studyGame(a)
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
        if ans != 'go' or (ans == 'go' and not specs and wReason[0] == False): 
            if ans != 'go':
                ans3 = input(inpString).lower()
            else:
                ans3 = "random game"
            if ans3 in searchOptions: 
                if ans3 == "random game":
                    print("\n" + YELLOW + "A random game will be chosen." + RESET + "\n")
                    ans2 = "random"
                    pickedGame = random.randint(0, len(gameData)-1)
                    print("Searching...\n")
                    return 
                    # completeSearch("go")
                else: 
                    ans2 = input(YELLOW + "\nWhich " + ans3 + " would you like to select?\n\n" + RESET)
                    print()
                    if ans3 == 'month': 
                        if ans2 in monthNames:
                            catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                            print(YELLOW + "You have selected " + ans2 + " as a month." + RESET + "\n")
                            ans2 = monthNums[monthNames.index(ans2)]
                            #print("ans3: " + ans3)
                            #print("ans : " + ans)
                            #print(catList)
                            if specs and ans3 == ans and ans3 not in catList:
                                specs.remove(specs[len(specs)-1])
                            specs.append((ans3, ans2)) 
                        else:
                            print(YELLOW + "That's not a valid month." + RESET + "\n")
                        completeSearch(ans3) 
                    elif ans3 == 'year':
                        if ans2 in validYears:
                            catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                            if specs and ans3 == ans and ans3 not in catList:
                                specs.remove(specs[len(specs)-1])
                            specs.append((ans3, ans2)) 
                            print(YELLOW + "You have chosen the year " + ans2 + "." + RESET + "\n")
                        else:
                            print(YELLOW + "That's not a valid year." + RESET + "\n")
                        completeSearch(ans3)
                    elif ans3 == 'day':
                        try:
                            if int(ans2) > 0 and int(ans2) < 32:
                                catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                                if specs and ans3 == ans and ans3 not in catList:
                                    specs.remove(specs[len(specs)-1])
                                specs.append((ans3, ans2)) 
                                print(YELLOW + "You have chosen " + ans2 + " as a day." + RESET + "\n")
                            else:
                                print(YELLOW + "That's not a valid day." + RESET + "\n")
                                
                        except:
                            print(YELLOW + "That's not a valid day." + RESET + "\n")
                        completeSearch(ans3)
                    elif ans3 == 'home_team' or ans3 == 'away_team':
                        if ans2 in {x[5] for x in teamData}:
                            catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                            if specs and ans3 == ans and ans3 not in catList:
                                specs.remove(specs[len(specs)-1])
                            specs.append((ans3, ans2))
                        else:
                            print(YELLOW + "That's not a valid team." + RESET + "\n")
                        completeSearch(ans3)
                    else:
                        # if newly entered searchOption is already lingering in specs, update it
                        if specs and ans3 == ans and ans3 not in catList:
                            specs.remove(specs[-1])
                            catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                        # don't append special categories
                        if ans3 != "win_reason" and ans3 != "ptpr":
                            specs.append((ans3, ans2))
                            catList[searchOptions.index(ans3)] = "*" + ans2 + "*" 
                        elif ans3 == "ptpr":
                            # perf = [True, ans2.split(":")[0], ans2.split(":")[1]]
                            allPlayers = {x[0] for x in playerData}
                            anyPMode = False
                            anyTMode = False
                            careerMode = False
                            if ans2.count(":") > 0:
                                wlTrans = {"W": " and won", "L": " and lost", "any": ""}
                                a2Parts = ans2.split(":")
                                tTrans = {True: "", False: " for the " + a2Parts[1]}
                                if ans2.count(":") == 1 and a2Parts[1] == "career":
                                    careerMode = True
                                    specs.append((ans3, ans2))
                                    catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                                    print(YELLOW + "You want to look all games that feature " + a2Parts[0] + ".\n" + RESET)
                                if a2Parts[0] == "any":
                                    anyPMode = True 
                                if a2Parts[1] == "any":
                                    anyTMode = True 
                                if a2Parts[0] in allPlayers or anyPMode:
                                    if a2Parts[1] in {x[5] for x in teamData} or anyTMode:
                                        if "<" in a2Parts[2] or anyTMode:
                                            if a2Parts[2].split("<")[0] in legalPStats or anyTMode:
                                                specs.append((ans3, ans2))
                                                catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                                                print(YELLOW + "You want to look at games" + tTrans[anyTMode] + " where "
                                                + a2Parts[0] + " performed " + a2Parts[2] + wlTrans[a2Parts[3]] + ".\n" + RESET)
                                            else:
                                                print(YELLOW + "That's not a valid stat. Legal stats are shown below:\n" + str(legalStats) + RESET + "\n")
                                        elif ">" in a2Parts[2] or anyTMode:
                                            if a2Parts[2].split(">")[0] in legalPStats or anyTMode:
                                                specs.append((ans3, ans2))
                                                catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                                                print(YELLOW + "You want to look at games" + tTrans[anyTMode] + " where "
                                                + a2Parts[0] + " performed " + a2Parts[2] + wlTrans[a2Parts[3]] + ".\n" + RESET)
                                            else:
                                                print(YELLOW + "That's not a valid stat. Legal stats are shown below:\n" + str(legalStats) + RESET + "\n")
                                    elif not careerMode:
                                        print(YELLOW + "That's not a valid team." + RESET + "\n")
                                else:
                                    print(YELLOW + "That's not a valid player." + RESET + "\n")
                            else:
                                print(YELLOW + "Please answer in the format 'Player Name:Team:Performance:Result'." + RESET + "\n")
                                print(YELLOW + "You can also use the format 'Player Name:career' for all games played by the player." + RESET + "\n")
                        elif ans3 == "win_reason":
                            if ":" in ans2:
                                if ans2.split(":")[1] in legalStats:
                                    wReason[0] = (True, ans2.split(":")[0], ans2.split(":")[1])
                                    catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                                    print(YELLOW + "You have chosen " + ans2.split(":")[0] + " games that were "
                                    + "won because of " + ans2.split(":")[1] + "." + RESET + "\n")
                            elif ans2 in legalStats:
                                wReason[0] = (True, "any", ans2)
                                catList[searchOptions.index(ans3)] = "*" + ans2 + "*"
                                print(YELLOW + "You have chosen games that were "
                                    + "won because of " + ans2 + "." + RESET + "\n")
                            else:
                                print(YELLOW + "Please answer using the format \"home/away:stat\"." + RESET + "\n")
                        completeSearch(ans3) 
            elif ans3 != 'go':
                if ans3 == "random":
                    print("\n" + YELLOW + "A random game will be chosen." + RESET + "\n")
                    ans2 = "random"
                    pickedGame = random.randint(0, len(gameData)-1)
                    completeSearch("go")
                elif ans3 == "quit":
                    print("\nQuitting... \n")
                    quit()
                else:
                    print("\n" + YELLOW + "I'm sorry, I didn't quite get that.\n" + RESET) 
                    completeSearch(ans3)
            else:
                print()
                completeSearch(ans3)
        else:
            print("Searching...\n")
            return 
    
    # create set of all player performances, keep those that meet criteria
    def createPlayerSet(on):
        # perfData = ["Ben Simmons", "76ers", "TO>5", "L"]
        teamTrans = {x[4] : x[5] for x in teamData}
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
                    if perfData[1] == "any":
                        addString += "any:"
                    else:
                        addString += teamTrans[gameDetails[i][2]] + ":"

                    if ">" in perfData[2]:
                        pStat = perfData[2].split(">")[0]
                        statVal = perfData[2].split(">")[1]
                        if gameDetails[i][playerInfo.index(pStat)] != "":
                            if float(gameDetails[i][playerInfo.index(pStat)]) > float(statVal):
                                # print(float(gameDetails[i][playerInfo.index(pStat)]))
                                # perfData[0] = gameDetails[i][5]
                                addString += perfData[2] + ":"
                    elif "<" in perfData[2]:
                        pStat = perfData[2].split("<")[0]
                        statVal = perfData[2].split("<")[1]
                        if gameDetails[i][playerInfo.index(pStat)] != "":
                            if float(gameDetails[i][playerInfo.index(pStat)]) < float(statVal):
                                # print(float(gameDetails[i][playerInfo.index(pStat)]))
                                # perfData[0] = gameDetails[i][5]
                                addString += perfData[2] + ":"
                    else:
                        addString += "any:"
                    addString += perfData[3]

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
                coll.append(display(False, gameList, x, gameData, teamData, gameDetails, playerInfo, ans1, ans2, specs, "")) 
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
    searchOptions = ["year","month","day","home_team","away_team","win_reason","ptpr","random game"]
    # lowercase version of searchOptions
    #searchOpLower = [x.lower() for x in searchOptions]
    # display version of searchOptions
    searchOpDis = ["year","month","day","home_team","away_team","win_reason","ptpr","random_game"]
    catList = ["?","?","?","?","?","?","?","?","?"]
    searchI = [0,0,0,3,4,1,1]
    legalStats = ["FG_PCT","FG3_PCT","FT_PCT","FTA","AST","REB","STL","BLK","TO"]
    legalPStats = ["MIN","FGM","FGA","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA",
                   "FT_PCT","OREB","DREB","REB","AST","STL","BLK","TO","PF","PTS","PLUS_MINUS"]
    validYears = [str(2002 + i) for i in range(1, 22)]
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

    # if ptpr in specs, parse, also translate "career" if present
    perfData = []
    playerParam = False
    for x in specs:
        pCareer = x
        if "ptpr" in x:
            if "career" in x[1]:
                specs.remove(x)
                pCareer = (x[0], x[1][:x[1].index(":")] + ":any:any:any")
                specs.append(pCareer)
            perfData = pCareer[1].split(":")
            playerParam = True

    # specs are fully ready

    print("Finding games that meet the parameters...\n")
            
    # create set of all player performances
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
                #print(x)
                #if specs[j][1].split(":")[0] == "any":
                    #if x.split(":")[2] in pSet:
                        #specs[j][1] = str()
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
    ws = 0
    ls = 0

    rand = False
    plperf = False
    tf = ""
    finalTf = ""
    finalPerf = ""
    finalAction = ""

    for x in specs:
        if "year" in x:
            tf = x[1]
        if "ptpr" in x:
            plperf = True
            playerName = x[1].split(":")[0]
            team = x[1].split(":")[1]
            performance = x[1].split(":")[2]
            result = x[1].split(":")[3]

    print("Displaying results...\n")
    
    if not specs:
        gameList.clear()
        rand = True
    
    allTeams = []
    for i in range(len(teamData)): # -4 ???
        allTeams.append(teamData[i][5])
    sortTeams = sorted(allTeams)

    # ['76ers-45m', 'Bucks-106m', 'Bulls-160m', 'Cavaliers-88m', 'Celtics-34m', 'Clippers-203m', 'Grizzlies-86m', 
    # 'Hawks-9m', 'Heat-198m', 'Hornets-87m', 'Jazz-148m', 'Kings-98m', 'Knicks-202m', 'Lakers-129m', 'Magic-33m', 
    # 'Mavericks-27m', 'Nets-153m', 'Nuggets-220m', 'Pacers-226m', 'Pelicans-216m', 'Pistons-198m', 'Raptors-1m', 
    # 'Rockets-196m', 'Spurs-245m', 'Suns-214m', 'Thunder-166m', 'Timberwolves-46m', 'Trail Blazers-124m', 
    # 'Warriors-221m', 'Wizards-69m']

    teamColors = ['45m','106m','160m','88m','34m','203m','86m','9m','198m','87m','148m','98m','202m','129m','33m',
                '27m','153m','220m','226m','216m','198m','1m','196m','245m','214m','166m','46m','124m','221m','69m']

    playerTeams = set()

    # get wNick, lNick, wColor, lColor, and you're free from extra display!!!
    for x in gameList:  
        homePts = gameData[x][7]
        homeTeam = gameData[x][3]
        awayPts = gameData[x][14]
        awayTeam = gameData[x][4]
        wTeam = ""
        wPts = ""
        lTeam = ""
        lPts = ""
        lNick = "" # validGame[2]
        wNick = "" # validGame[0]
        date = gameData[x][0] # validGame[-1]
        season = gameData[x][5]
        awayNick = "" # validGame[-2]
        homeNick = "" # validGame[-3
        wColor = "" # validGame[-4]
        lColor = "" # validGame[-5]
        # teamSeasons = []
        if float(homePts) > float(awayPts):
            wTeam = homeTeam
            wPts = str(int(float(homePts)))
            lTeam = awayTeam
            lPts = str(int(float(awayPts)))
        else:
            wTeam = awayTeam
            wPts = str(int(float(awayPts)))
            lTeam = homeTeam
            lPts = str(int(float(homePts)))
        for y in teamData:
            if y[1] == wTeam:
                wNick = y[5]
            if y[1] == lTeam:
                lNick = y[5]
            if y[1] == homeTeam:
                homeNick = y[5]
            if y[1] == awayTeam:
                awayNick = y[5]
        wColor = teamColors[sortTeams.index(wNick)]
        lColor = teamColors[sortTeams.index(lNick)]
        homeColor = teamColors[sortTeams.index(homeNick)]
        awayColor = teamColors[sortTeams.index(awayNick)]

        if plperf:
            teamSeasons = []
            if team != "any":
                for i in range(2003, 2022):
                    teamSeasons.append(([team], str(i)))
                if wNick == team: # for validGame, + " "
                    ws += 1
                elif lNick == team:
                    ls += 1
            else:
                maxSeason = ("", 0)
                minSeason = ("", 1000000)
                for p in playerData:
                    if playerName in p:
                        teamSeasons.append(([y[5] for y in teamData if y[1] == p[1]], p[3]))
                for t in teamSeasons:
                    if int(list(t[1])[0]) > int(maxSeason[1]):
                        maxSeason = (t[0], t[1])
                        # print("Max: " + str(maxSeason))
                    if int(list(t[1])[0]) < int(minSeason[1]):
                        minSeason = (t[0], t[1])
                        # print("Min: " + str(minSeason))
                
                i = int(maxSeason[1])+1
                #print(i)
                while i < 2021:
                    teamSeasons.insert(0, (maxSeason[0], str(i)))
                    i += 1
                j = int(minSeason[1])-1
                #print(j)
                while j > 2002:
                    teamSeasons.append((minSeason[0], str(j)))
                    j -= 1

                for y in teamSeasons:
                    if playerTeams:
                        playerTeams.add(y[0][0])

                if ([wNick], list({y[5] for y in gameData if y[0] == date})[0]) in teamSeasons:
                    ws += 1
                elif ([lNick], list({y[5] for y in gameData if y[0] == date})[0]) in teamSeasons:
                    ls += 1

        homeColOG = "\033[1;38;5;" + homeColor
        awayColOG = "\033[1;38;5;" + awayColor
        wColOG= "\033[1;38;5;" + wColor
        lColOG = "\033[1;38;5;" + lColor
        playerWin = ""
        playerLoss = ""
        unNecG = 0
        unNecW = 0
        unNecL = 0
        # print(([wNick], str(season)))
        # print()
        # print(teamSeasons)
        if plperf:
            unNecL -= 7
            if ([wNick], str(season)) in teamSeasons:
                playerWin = BGREEN
                unNecW -= 7
                unNecL += 9
            else:
                playerWin = ""
            if ([lNick], str(season)) in teamSeasons:
                playerLoss = BRED
                unNecL += 2
            else:
                playerLoss = ""
        if len(homeColor) == 2:
            unNecG += 2
        elif len(homeColor) == 3:
            unNecG += 1
        if len(awayColor) == 2:
            unNecG += 2
        elif len(awayColor) == 3:
            unNecG += 1
        if len(wColor) == 2:
            unNecW += 2
        elif len(wColor) == 3:
            unNecW += 1
        if len(lColor) == 2:
            unNecL += 2
        elif len(lColor) == 3:
            unNecL += 1
        gameInfo = str(date + " (" + homeColOG + homeNick + RESET + " @ " + awayColOG + awayNick + RESET + ")").ljust(70-(unNecG), " ")
        winInfo = str(playerWin + "W" + RESET + ": " + wColOG + wNick + RESET).ljust(40-(unNecW), " ")
        lossInfo = str(playerLoss + "L" + RESET + ": " + lColOG + lNick + RESET).ljust(40-(unNecL), " ")
        winPtInfo = " (" + wPts + "-"
        lossPtInfo = lPts + ")"
        finalGameHeader = gameInfo + winInfo + lossInfo + winPtInfo + lossPtInfo
        resultList.append(finalGameHeader)
    resultList = list(set(resultList))
    tempList = []
    for i in range(len(resultList)):
        for j in range(len(gameList)):
            if resultList[i][:10] == gameData[gameList[j]][0]:
                tempList.append((resultList[i], gameList[j]))
                break

    tempList = sorted(tempList, key=lambda tup:tup[0])
    finalResultList = [x[0] for x in tempList]
    gameList = [x[1] for x in tempList]
    amend = False
    goBack = False
    for i in range(len(finalResultList)):
        if i < 9:
            print(str(i+1) + ":    " + finalResultList[i]) 
        elif i < 99:
            print(str(i+1) + ":   " + finalResultList[i])
        elif i < 999:
            print(str(i+1) + ":  " + finalResultList[i])
        else:
            print(str(i+1) + ": " + finalResultList[i])
    if len(gameList) != 0:
        print("\n" + str(len(finalResultList)) + " games found!\n")
        if plperf:
            finalTeam = " as a member of the " + team
            finalTf = ""
            winPerc = round(float(ws)/len(gameList), 2)
            if winPerc == 0.0:
                finalResult = " won " + str(winPerc)[0] + "% of games"
            elif winPerc == 1.0:
                finalResult = " won " + str(winPerc)[0] + "00" + "% of games"
            elif (winPerc*100) % 10 == 0:
                finalResult = " won " + str(winPerc)[2:] + "0" + "% of games"
            else:
                finalResult = " won " + str(winPerc)[2:] + "% of games"
            finalPerf = " when performing " + performance
            if team == "any":
                finalTeam = ""
            if tf != "":
                finalTf = " in " + tf
            if result == "L":
                finalResult = " lost " + str(round(float(ls)/len(gameList), 2))[2:] + "% of games"
            if result == "any":
                finalResult = " won " + str(ws) + " out of " + str(len(gameList)) + " games (" + str(round(float(ws)/len(gameList), 2)*100) + "%)"
            if performance == "any":
                finalPerf = ""
            print(playerName + finalTeam + finalTf + finalResult + finalPerf + ".\n")
            # Report player's career winning/losing percentage and compare!
        oneOrMany = "a game from the list"
        if len(gameList) == 1:
            oneOrMany = "the game"
        while True:
            gamePicked = False
            repAns = input(YELLOW + "Do you want to analyze " + oneOrMany + " (y or n or quit)?\n\n" + RESET)
            if repAns.lower() == "y":
                if len(gameList) != 1:
                    while not gamePicked:
                        gameNo = input(YELLOW + "\nWhich game from the list would you like to analyze?\n\n" + RESET)
                        try: 
                            if int(gameNo) > 0 and int(gameNo) < len(gameList)+1:
                                pickedGame = gameList[int(gameNo)-1]
                                gamePicked = True
                            else:
                                print(YELLOW + "\nPlease enter a number in the range 1-" + str(len(gameList)) + "." + RESET)
                        except:
                            if gameNo.lower() == "any":
                                randGame = random.randrange(len(gameList)-1)
                                pickedGame = gameList[randGame]
                                print("\n" + YELLOW + "Game " + str(randGame+1) + " chosen!\n" + RESET)
                                gamePicked = True
                            else:
                                print(YELLOW + "\nPlease enter a number in the range 1-" + str(len(gameList)) + "." + RESET)
                else:
                    pickedGame = gameList[0]
                break
            elif repAns.lower() == "n":
                goBack = True
                break
            elif repAns.lower() == "quit":
                print("\nQuitting...\n")
                quit()
            else:
                print("\n" + YELLOW + "I'm sorry, I didn't quite get that.\n" + RESET)
    else:
        if not rand:
            while True:
                amendAns = input("Sorry, no games found. Would you like to amend your search? (y or n or quit)\n\n")
                if amendAns.lower() == "y":
                    specs.clear()
                    amend = True
                    print()
                    break
                elif amendAns.lower() == "n":
                    specs.clear()
                    goBack = True
                    print()
                    break
                elif amendAns.lower() == "quit":
                    print("\nQuitting...\n")
                    break
                    quit()
                else:
                    print("\n" + YELLOW + "I'm sorry, I didn't quite get that.\n" + RESET)
        else:
            ans2 = "random"
            specs.clear()
        pickedGame = random.randint(0, len(gameData)-1)

    # display analysis of picked game
    q = ""
    if wReason[0][0]:
        specs.append(("winReason", wReason[0][1] + ":" + wReason[0][2]))
    if not amend and not goBack and not rand:
        q = "y"
        display(True, gameList, pickedGame, gameData, teamData, gameDetails, playerInfo, ans1, ans2, specs, q)
    elif not rand:
        q = "n"
        display(True, gameList, pickedGame, gameData, teamData, gameDetails, playerInfo, ans1, ans2, specs, q)
    else:
        display(True, gameList, pickedGame, gameData, teamData, gameDetails, playerInfo, ans1, ans2, specs, q)

# gets general database info stored
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
