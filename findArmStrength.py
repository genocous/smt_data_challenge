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
from IPython.display import display

#Courtesy of Eddie Dew's work in animation.py
from animation import plot_animation


#Uncomment the path for your local computer
#Arm Strength only calculated for throws from SS to 1B
def findSSthrows():
    #testing one player for now
    SSdf = pd.read_csv('shortstops.csv')
    temp = SSdf.iloc[1]
    ID = temp['Player_IDs']
    year = temp['Year']
    if(year == 1883):   
        game_info_subset = readDataSubset('game_info', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        game_info = game_info_subset.to_table(filter = (pads.field('Season') == "Season_1883")).to_pandas()

        game_events_subset = readDataSubset('game_events', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        game_events = game_events_subset.to_table(filter = (pads.field('Season') == "Season_1883")).to_pandas()

        player_position_subset = readDataSubset('player_pos', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        player_position_SS = player_position_subset.to_table(filter = (pads.field('Season') == "Season_1883") & (pads.field('player_position') == 6)).to_pandas()
        player_position_1B = player_position_subset.to_table(filter = (pads.field('Season') == "Season_1883") & (pads.field('player_position') == 3)).to_pandas()
    else:
        game_info_subset = readDataSubset('game_info', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        game_info = game_info_subset.to_table(filter = (pads.field('Season') == "Season_1884")).to_pandas()

        game_events_subset = readDataSubset('game_events', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        game_events = game_events_subset.to_table(filter = (pads.field('Season') == "Season_1884")).to_pandas()

        player_position_subset = readDataSubset('player_pos', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
        player_position_SS = player_position_subset.to_table(filter = (pads.field('Season') == "Season_1884") & (pads.field('player_position') == 6)).to_pandas()
        player_position_1B = player_position_subset.to_table(filter = (pads.field('Season') == "Season_1884") & (pads.field('player_position') == 3)).to_pandas()

    FirstBasecatches = game_events[(game_events['event_code'] == 2) & (game_events['player_position'] == 3)
                                     & (game_events.event_code.shift(1) == 3) & (game_events['player_position'].shift(1) == 6)]
    PlayerPlays = game_info[game_info['shortstop'] == ID]
    PlayerCatches = pd.merge(FirstBasecatches, PlayerPlays, on=["game_str", "at_bat", "play_per_game"], how="inner")
    PlayerCatches = PlayerCatches[["game_str", "play_id", "play_per_game"]]
    
    SSfields = game_events[(game_events['event_code'] == 3) & (game_events['player_position'] == 6)]
    PlayerCatchesWithTimestamps = pd.merge(PlayerCatches, SSfields, on=["game_str", "play_per_game"], how="left")
    PlayerCatchesWithTimestamps = PlayerCatchesWithTimestamps[["game_str", "play_id_x", "play_per_game", "timestamp"]]
    PlayerCatchesWithTimestamps = PlayerCatchesWithTimestamps.rename(columns={'timestamp':'start_time', 'play_id_x':'play_id'})
    PlayerCatchesWithTimestamps = pd.merge(PlayerCatchesWithTimestamps, FirstBasecatches, on=["game_str", "play_per_game"], how="left")
    PlayerCatchesWithTimestamps = PlayerCatchesWithTimestamps[["game_str", "play_id_x", "play_per_game", "start_time", "timestamp"]]
    PlayerCatchesWithTimestamps = PlayerCatchesWithTimestamps.rename(columns={'timestamp':'end_time', 'play_id_x':'play_id'})
    PlayerCatchesWithTimestamps['throw_time'] = (PlayerCatchesWithTimestamps['end_time'] - PlayerCatchesWithTimestamps['start_time']) / 1000
    # PlayerCatchesWithTimestamps['x_position_SS'] = 0
    # PlayerCatchesWithTimestamps['y_position_SS'] = 0
    # PlayerCatchesWithTimestamps['x_position_1B'] = 0
    # PlayerCatchesWithTimestamps['y_position_1B'] = 0
    PlayerCatchesWithTimestamps['distance'] = 0
    PlayerCatchesWithTimestamps['ft/sec'] = 0
    PlayerCatchesWithTimestamps['mph'] = 0

    pd.options.mode.chained_assignment = None
    for play in range(len(PlayerCatchesWithTimestamps)):
        print(play, "/", len(PlayerCatchesWithTimestamps))
        SSpos = player_position_SS[(player_position_SS['game_str'] == PlayerCatchesWithTimestamps['game_str'].iloc[play]) &
                                   (player_position_SS['play_id'] == PlayerCatchesWithTimestamps['play_id'].iloc[play]) &
                                   (player_position_SS['player_position'] == 6) &
                                   (player_position_SS['timestamp'] >= PlayerCatchesWithTimestamps['start_time'].iloc[play]) &
                                   (player_position_SS['timestamp'] <= PlayerCatchesWithTimestamps['end_time'].iloc[play])]
        pos1B = player_position_1B[(player_position_1B['game_str'] == PlayerCatchesWithTimestamps['game_str'].iloc[play]) &
                                   (player_position_1B['play_id'] == PlayerCatchesWithTimestamps['play_id'].iloc[play]) &
                                   (player_position_1B['player_position'] == 3) &
                                   (player_position_1B['timestamp'] >= PlayerCatchesWithTimestamps['start_time'].iloc[play]) &
                                   (player_position_1B['timestamp'] <= PlayerCatchesWithTimestamps['end_time'].iloc[play])]
        # PlayerCatchesWithTimestamps.at[play, 'x_position_SS'] = SSpos['field_x'].iloc[0]
        # PlayerCatchesWithTimestamps.at[play, 'y_position_SS'] = SSpos['field_y'].iloc[0]
        # PlayerCatchesWithTimestamps.at[play, 'x_position_1B'] = pos1B['field_x'].iloc[0]
        # PlayerCatchesWithTimestamps.at[play, 'y_position_1B'] = pos1B['field_y'].iloc[0]
        distanceSSto1B = np.sqrt((SSpos['field_x'].iloc[0] - pos1B['field_x'].iloc[0])**2. + 
                                (SSpos['field_y'].iloc[0] - pos1B['field_y'].iloc[0])**2.)
        PlayerCatchesWithTimestamps['distance'].iloc[play] = distanceSSto1B
        ftsec = distanceSSto1B / PlayerCatchesWithTimestamps['throw_time'].iloc[play]
        PlayerCatchesWithTimestamps['ft/sec'].iloc[play] = ftsec
        mph = ftsec / 1.467
        PlayerCatchesWithTimestamps['mph'].iloc[play] = mph

    print(PlayerCatchesWithTimestamps)
    
    #animation check
    # player_position_df = player_position_subset.to_table(filter = (pads.field('game_str') == "1883_011_Vis4AE_Home4A")).to_pandas()
    # ball_position_subset = readDataSubset('ball_pos', "/Users/andy/Desktop/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge")
    # ball_position_df = ball_position_subset.to_table(filter = (pads.field('game_str') == "1883_011_Vis4AE_Home4A")).to_pandas()
    # hi = plot_animation(player_position_df, ball_position_df, 3, False)
    # with open("animation.html", "w") as file:
    #     file.write(hi.data)

    # for index, row in SSdf.iterrows():
    #     ID = row['Player_IDs']
    #     year = row['Year']
    #     level = row['Level']


def main():
      findSSthrows()

if __name__ == "__main__":
    main()



