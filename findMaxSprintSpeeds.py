# Find max sprint speed for each relevant player
# Measured in ft/sec
# For now: only from baserunning
# Calculates velocity based on how far the player moves every 1 second in accordance with the statcast sprint speed metric (see below)
# https://baseballsavant.mlb.com/leaderboard/sprint_speed
# Adds results to .csv files

import pandas as pd
import numpy as np
import os
import csv

file_path = ""
game_info = ""
game_events = ""

#Set file_paths to your path to the folders within the player_pos folder
file_path_1883_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home1A"
file_path_1883_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home2A"
file_path_1883_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home3A"
file_path_1883_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home4A"
file_path_1884_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home1A"
file_path_1884_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home2A"
file_path_1884_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home3A"
file_path_1884_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home4A"

#Set file_paths to your path to the folders within the game_info folder
game_info_1883_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info/Season_1883/Home1A"
game_info_1883_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info/Season_1883/Home2A"
game_info_1883_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info/Season_1883/Home3A"
game_info_1883_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info/Season_1883/Home4A"
game_info_1884_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info/Season_1884/Home1A"
game_info_1884_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info/Season_1884/Home2A"
game_info_1884_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info/Season_1884/Home3A"
game_info_1884_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info/Season_1884/Home4A"

#Set file_paths to your path to the folders within the game_events folder
game_events_1883_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_events/Season_1883/Home1A"
game_events_1883_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_events/Season_1883/Home2A"
game_events_1883_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_events/Season_1883/Home3A"
game_events_1883_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_events/Season_1883/Home4A"
game_events_1884_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_events/Season_1884/Home1A"
game_events_1884_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_events/Season_1884/Home2A"
game_events_1884_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_events/Season_1884/Home3A"
game_events_1884_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_events/Season_1884/Home4A"

def findMaxSprintSpeed(Player_ID, file_path, game_info, game_events):
    plays = Conversion(findRelevantPlays(game_info, Player_ID), game_events) #finds the plays that the given player is running the bases or batting in
    for i in range (2, 6): #minor data fixing
        if(plays.iloc[0, i] == 1.0):
            plays.iloc[0, i] = True
        else:
            plays.iloc[0, i] = False
    max_sprint_speed = 0
    sprint_speed = 0
    c = 0
    for root, dirs, files in os.walk(file_path):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        if((plays.iloc[c, 0] == row[0]) & (plays.iloc[c, 1] == row[1])): #if the current line is the start of a selected play
                            data = {'timestamp': [], 'x_pos': [], 'y_pos': []}
                            df = pd.DataFrame(data)
                            if(plays.iloc[c, 2]): #if the player is batting
                                while(plays.iloc[c, 1] == row[1]): #while the same play is happening
                                    try: #try/except to prevent the reader from going out of bounds
                                        if(row[3] == '10'):
                                            new_row = {'timestamp': row[2], 'x_pos': row[4], 'y_pos': row[5]}
                                            new_row_df = pd.DataFrame([new_row])
                                            df = pd.concat([df, new_row_df], ignore_index=True)
                                        row = next(csv_reader)
                                    except StopIteration:
                                        break
                            elif(plays.iloc[c, 3]): #if the player is on 1B
                                while(plays.iloc[c, 1] == row[1]):
                                    try:
                                        if(row[3] == '11'):
                                            new_row = {'timestamp': row[2], 'x_pos': row[4], 'y_pos': row[5]}
                                            new_row_df = pd.DataFrame([new_row])
                                            df = pd.concat([df, new_row_df], ignore_index=True)
                                        row = next(csv_reader)
                                    except StopIteration:
                                        break
                            elif(plays.iloc[c, 4]): #if the player is on 2B
                                while(plays.iloc[c, 1] == row[1]):
                                    try:
                                        if(row[3] == '12'):
                                            new_row = {'timestamp': row[2], 'x_pos': row[4], 'y_pos': row[5]}
                                            new_row_df = pd.DataFrame([new_row])
                                            df = pd.concat([df, new_row_df], ignore_index=True)
                                        row = next(csv_reader)
                                    except StopIteration:
                                        break
                            else: #if the player is on 3B
                                while(plays.iloc[c, 1] == row[1]):
                                    try:
                                        if(row[3] == '13'):
                                            new_row = {'timestamp': row[2], 'x_pos': row[4], 'y_pos': row[5]}
                                            new_row_df = pd.DataFrame([new_row])
                                            df = pd.concat([df, new_row_df], ignore_index=True)
                                        row = next(csv_reader)
                                    except StopIteration:
                                        break

                            df['timestamp'] = df['timestamp'].astype(int)
                            df['x_pos'] = df['x_pos'].astype(float)
                            df['y_pos'] = df['y_pos'].astype(float)

                            # Calculate differences between points 2 seconds apart
                            df['delta_x'] = df['x_pos'].diff(periods=40)
                            df['delta_y'] = df['y_pos'].diff(periods=40)
                            df['delta_t'] = df['timestamp'].diff(periods=40)

                            # Calculate the displacement (Euclidean distance) and velocity
                            df['displacement'] = np.sqrt(df['delta_x']**2 + df['delta_y']**2)
                            df['velocity'] = (df['displacement'] / df['delta_t']) * 1000 #multiply by 1000 to adjust from ms to sec

                            df['displacement'] = df['displacement'].astype(float)
                            df['velocity'] = df['velocity'].astype(float)

                            # Find the maximum velocity
                            sprint_speed = df['velocity'].max()
                            if(sprint_speed > max_sprint_speed):
                                max_sprint_speed = sprint_speed
                            if(c < (len(plays) - 1)): 
                                c = c + 1                          
    print(max_sprint_speed.astype(float))
    return(max_sprint_speed.astype(float))

def findRelevantPlays(game_info, Player_ID):
    data = {'game_str': [], 'play_id': [], 'Batter': [],'1B': [],'2B': [], '3B': []}
    df = pd.DataFrame(data)
    for root, dirs, files in os.walk(game_info):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        if(row[6] == "bottom"):
                            if(row[16] == str(Player_ID)):
                                new_row = {'game_str': row[0], 'play_id': row[4], 'Batter': True,'1B': False,'2B': False, '3B': False}
                                new_row_df = pd.DataFrame([new_row])
                                df = pd.concat([df, new_row_df], ignore_index=True)
                            if(row[17] == str(Player_ID)):
                                new_row = {'game_str': row[0], 'play_id': row[4], 'Batter': False,'1B': True,'2B': False, '3B': False}
                                new_row_df = pd.DataFrame([new_row])
                                df = pd.concat([df, new_row_df], ignore_index=True)
                            if(row[18] == str(Player_ID)):
                                new_row = {'game_str': row[0], 'play_id': row[4], 'Batter': False,'1B': False,'2B': True, '3B': False}
                                new_row_df = pd.DataFrame([new_row])
                                df = pd.concat([df, new_row_df], ignore_index=True)
                            if(row[19] == str(Player_ID)):
                                new_row = {'game_str': row[0], 'play_id': row[4], 'Batter': False,'1B': False,'2B': False, '3B': True}
                                new_row_df = pd.DataFrame([new_row])
                                df = pd.concat([df, new_row_df], ignore_index=True)
    return(df)

def Conversion(df, game_events): #converts from play_per_game to play_id
    c = 0
    for root, dirs, files in os.walk(game_events):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        if((df.iloc[c, 0] == row[0]) & (df.iloc[c, 1] == row[3])):
                            df.iloc[c, 1] = row[1]
                            if(c < (len(df) - 1)):
                                c = c + 1
    return(df)

def setPaths(Level, Year):
    if(Year == 1883):
        if(Level == 1):
            file_path = file_path_1883_1
            game_info = game_info_1883_1
            game_events = game_events_1883_1
        elif(Level == 2):
            file_path = file_path_1883_2
            game_info = game_info_1883_2
            game_events = game_events_1883_2
        elif(Level == 3):
            file_path = file_path_1883_3
            game_info = game_info_1883_3
            game_events = game_events_1883_3
        else:
            file_path = file_path_1883_4
            game_info = game_info_1883_4
            game_events = game_events_1883_4
    else:
        if(Level == 1):
            file_path = file_path_1884_1
            game_info = game_info_1884_1
            game_events = game_events_1884_1
        elif(Level == 2):
            file_path = file_path_1884_2
            game_info = game_info_1884_2
            game_events = game_events_1884_2
        elif(Level == 3):
            file_path = file_path_1884_3
            game_info = game_info_1884_3
            game_events = game_events_1884_3
        else:
            file_path = file_path_1884_4
            game_info = game_info_1884_4
            game_events = game_events_1884_4
    return [file_path, game_info, game_events]

def main():
    SSdf = pd.read_csv('shortstops.csv')
    CFdf = pd.read_csv('center_fielders.csv')
    SSCFdf = pd.read_csv('shortstop_and_center_fielders.csv')
    SSdf["Max_Sprint_Speed"] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    CFdf["Max_Sprint_Speed"] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    SSCFdf["Max_Sprint_Speed"] = [0,0]
    SSdf['Max_Sprint_Speed'] = SSdf['Max_Sprint_Speed'].astype(float)
    CFdf['Max_Sprint_Speed'] = CFdf['Max_Sprint_Speed'].astype(float)
    SSCFdf['Max_Sprint_Speed'] = SSCFdf['Max_Sprint_Speed'].astype(float)

    for index, row in SSdf.iterrows():
        ID = row['Player_IDs'] 
        Level = row['Level'] 
        Year = row['Year']
        paths = setPaths(Level, Year)
        SSdf.at[index, 'Max_Sprint_Speed'] = findMaxSprintSpeed(ID.astype(int), paths[0], paths[1], paths[2])
    SSdf.to_csv('shortstops.csv', index=False, header=True)

    for index, row in CFdf.iterrows():
        ID = row['Player_IDs'] 
        Level = row['Level'] 
        Year = row['Year']
        paths = setPaths(Level, Year)
        CFdf.at[index, 'Max_Sprint_Speed'] = findMaxSprintSpeed(ID.astype(int), paths[0], paths[1], paths[2])
    CFdf.to_csv('center_fielders.csv', index=False, header=True)

    for index, row in SSCFdf.iterrows():
        ID = row['Player_IDs'] 
        Level = row['Level'] 
        Year = row['Year']
        paths = setPaths(Level, Year)
        SSCFdf.at[index, 'Max_Sprint_Speed'] = findMaxSprintSpeed(ID.astype(int), paths[0], paths[1], paths[2])
    SSCFdf.to_csv('shortstop_and_center_fielders.csv', index=False, header=True)

    print("DONE NOW")

if __name__ == "__main__":
    main()