import pandas as pd
import numpy as np
from math import pi

import matplotlib.pyplot as plt
import seaborn as sns

games_details = pd.read_csv('data/games_details.csv')
players = pd.read_csv('data/players.csv')
teams = pd.read_csv('data/teams.csv')
ranking = pd.read_csv('data/ranking.csv')
games  = pd.read_csv('data/games.csv')

############################################################

df = games_details
# make data
player1 = input("Player 1?\n")
player2 = input("Player 2?\n")
player1CareerAvgs = round(df.query("PLAYER_NAME == @player1").loc[:,["PTS","FG3M","FG3A","REB","AST","STL","BLK"]].mean(), 2)
player2CareerAvgs = round(df.query("PLAYER_NAME == @player2").loc[:,["PTS","FG3M","FG3A","REB","AST","STL","BLK"]].mean(), 2)
# plot
fig, ax = plt.subplots()
ax.bar(["PTS","FG3M","FG3A","REB","AST","STL","BLK"], player1CareerAvgs, label=player1, width=-0.3, edgecolor="white", linewidth=2, align="edge")
ax.bar_label(ax.containers[0], fontsize=6)
ax.bar(["PTS","FG3M","FG3A","REB","AST","STL","BLK"], player2CareerAvgs, label=player2, width=0.3, edgecolor="white", linewidth=2, align="edge")
ax.bar_label(ax.containers[1], fontsize=6)
ax.legend(title="Player")
ax.set_title("Career Averages")
plt.show()

# TODO
# player1 vs. the average G/F/C