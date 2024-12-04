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
columns = df.columns.values.tolist()
player1 = input("Player 1?\n")
player2 = input("Player 2?\n")
stephStatAvgs = df.query("PLAYER_NAME == @player1").loc[:,["PTS","FG3M","FG3A","REB","AST","STL","BLK"]].mean()
lebronStatAvgs = df.query("PLAYER_NAME == @player2").loc[:,["PTS","FG3M","FG3A","REB","AST","STL","BLK"]].mean()
#plt.show()
print(stephStatAvgs)
print(lebronStatAvgs)



# display(Markdown('#### Stats comparison between Lebron James and overall statistics'))
# fig, ax = plt.subplots(figsize=(18, 9))

# ax = plt.subplot(121, polar=True)
# ax.set_title('Percentage statistics')
# radar_plot(ax=ax, df=stats_prct, max_val=1)

# ax = plt.subplot(122, polar=True)
# ax.set_title('Others statistics')
# radar_plot(ax=ax, df=stats_other, max_val=10)

# plt.show()