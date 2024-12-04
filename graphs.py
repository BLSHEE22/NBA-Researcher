import pandas as pd
import numpy as np
from math import pi

import matplotlib.pyplot as plt
import seaborn as sns

from IPython.display import display, Markdown

games_details = pd.read_csv('/data/games_details.csv')
players = pd.read_csv('/data/players.csv')
teams = pd.read_csv('/data/teams.csv')
ranking = pd.read_csv('/data/ranking.csv')
games  = pd.read_csv('/data/games.csv')

dataset_overview(games_details, 'games_details')