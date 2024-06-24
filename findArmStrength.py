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


#Set file_paths to your path to the folders within the player_pos folder 
#Uncomment the path for your local computer

#file_path_1883_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home1A"
#file_path_1883_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home2A"
#file_path_1883_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home3A"
#file_path_1883_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home4A"
#file_path_1884_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home1A"
#file_path_1884_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home2A"
#file_path_1884_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home3A"
#file_path_1884_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home4A"

# file_path_1883_1 = "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home1A"
# file_path_1883_2 = "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home2A"
# file_path_1883_3 = "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home3A"
# file_path_1883_4 = "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home4A"
# file_path_1884_1 = "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home1A"
# file_path_1884_2 = "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home2A"
# file_path_1884_3 = "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home3A"
# file_path_1884_4 = "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home4A"

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
    
    Player_gameinfo = game_info[game_info['shortstop'] == ID].game_str.unique()
    print(len(Player_gameinfo))

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



