# Find Arm Strengths of SS, SS/OF, and OF
# Measured based on average of top (5-10%) throws
# Measured based on velocity of throw in mph

import pandas as pd
import csv
import os
import numpy as np
from SMT_data_starter import readDataSubset
import matplotlib.pyplot as plt
import pyarrow.dataset as pads


#Uncomment the path for your local computer
#Arm Strength only calculated for throws from SS to 1B
def findSSthrows():
    #testing one player for now
    SSdf = pd.read_csv('shortstops.csv')
    temp = SSdf.iloc[1]
    ID = temp['Player_IDs']
    year = temp['Year']
    level = temp['Level']
    if(year == 1883):   
        game_info_subset = readDataSubset('game_info', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        game_info = game_info_subset.to_table(filter = (pads.field('Season') == "Season_1883")).to_pandas()

        game_events_subset = readDataSubset('game_events', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        game_events = game_events_subset.to_table(filter = (pads.field('Season') == "Season_1883")).to_pandas()
    else:
        game_info_subset = readDataSubset('game_info', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        game_info = game_info_subset.to_table(filter = (pads.field('Season') == "Season_1884")).to_pandas()

        game_events_subset = readDataSubset('game_events', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        game_events = game_events_subset.to_table(filter = (pads.field('Season') == "Season_1884")).to_pandas()

    SScatchesGrounders = game_events[(game_events['event_code'] == 2) & (game_events['player_position'] == 3)
                                     & (game_events.event_code.shift(1) == 3) & (game_events['player_position'].shift(1) == 6)]
    PlayerPlays = game_info[game_info['shortstop'] == ID]
    PlayerCatches = pd.merge(SScatchesGrounders, PlayerPlays, on=["game_str", "at_bat", "play_per_game"], how="inner")
    PlayerCatches = PlayerCatches[["game_str", "play_id", "play_per_game"]]
    PlayerCatches
    print(PlayerCatches)

    # for index, row in SSdf.iterrows():
    #     ID = row['Player_IDs']
    #     year = row['Year']
    #     level = row['Level']


def main():
      findSSthrows()

if __name__ == "__main__":
    main()



