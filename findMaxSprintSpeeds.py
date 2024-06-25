# Find max sprint speed for each relevant player
# Measured in ft/sec
# For now: only from baserunning
# Adds results to .csv flies

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
    plays = Conversion(findRelevantPlays(game_info, Player_ID), game_events)
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
                        if(plays.iloc(c, 0) == row[0] & plays.iloc(c, 1) == row[1]):
                            data = {'timestamp': [], 'x_pos': [], 'y_pos': []}
                            df = pd.DataFrame(data)
                            if(plays.iloc(c, 2)):
                                while(plays.iloc(c, 1) == row[1]):
                                    if(row[10]):
                                        new_row = {'timestamp': row[2], 'x_pos': row[4], 'y_pos': row[5]}
                                        new_row_df = pd.DataFrame([new_row])
                                        df = pd.concat([df, new_row_df], ignore_index=True)
                                    next(csv_reader)
                            elif(plays.iloc(c, 3)):
                                while(plays.iloc(c, 1) == row[1]):
                                    if(row[11]):
                                        new_row = {'timestamp': row[2], 'x_pos': row[4], 'y_pos': row[5]}
                                        new_row_df = pd.DataFrame([new_row])
                                        df = pd.concat([df, new_row_df], ignore_index=True)
                                    next(csv_reader)
                            elif(plays.iloc(c, 4)):
                                while(plays.iloc(c, 1) == row[1]):
                                    if(row[12]):
                                        new_row = {'timestamp': row[2], 'x_pos': row[4], 'y_pos': row[5]}
                                        new_row_df = pd.DataFrame([new_row])
                                        df = pd.concat([df, new_row_df], ignore_index=True)
                                    next(csv_reader)
                            else:
                                while(plays.iloc(c, 1) == row[1]):
                                    if(row[13]):
                                        new_row = {'timestamp': row[2], 'x_pos': row[4], 'y_pos': row[5]}
                                        new_row_df = pd.DataFrame([new_row])
                                        df = pd.concat([df, new_row_df], ignore_index=True)
                                    next(csv_reader)
                            # Calculate differences between consecutive points
                            df['delta_x'] = df['x_pos'].diff()
                            df['delta_y'] = df['y_pos'].diff()
                            df['delta_t'] = df['timestamp'].diff()

                            # Calculate the displacement (Euclidean distance) and velocity
                            df['displacement'] = np.sqrt(df['delta_x']**2 + df['delta_y']**2)
                            df['velocity'] = (df['displacement'] / df['delta_t']) * 1000

                            # Find the maximum velocity
                            sprint_speed = df['velocity'].max()
                            if(sprint_speed > max_sprint_speed):
                                max_sprint_speed = sprint_speed
                            c = c + 1
    return(max_sprint_speed)

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
                            if(row[16] == Player_ID):
                                new_row = {'game_str': row[0], 'play_id': row[4], 'Batter': True,'1B': False,'2B': False, '3B': False}
                                new_row_df = pd.DataFrame([new_row])
                                df = pd.concat([df, new_row_df], ignore_index=True)
                            if(row[17] == Player_ID):
                                new_row = {'game_str': row[0], 'play_id': row[4], 'Batter': False,'1B': True,'2B': False, '3B': False}
                                new_row_df = pd.DataFrame([new_row])
                                df = pd.concat([df, new_row_df], ignore_index=True)
                            if(row[18] == Player_ID):
                                new_row = {'game_str': row[0], 'play_id': row[4], 'Batter': False,'1B': False,'2B': True, '3B': False}
                                new_row_df = pd.DataFrame([new_row])
                                df = pd.concat([df, new_row_df], ignore_index=True)
                            if(row[19] == Player_ID):
                                new_row = {'game_str': row[0], 'play_id': row[4], 'Batter': False,'1B': False,'2B': False, '3B': True}
                                new_row_df = pd.DataFrame([new_row])
                                df = pd.concat([df, new_row_df], ignore_index=True)
    return(df)

def Conversion(df, game_events):
    c = 0
    for root, dirs, files in os.walk(game_events):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        if(df.iloc[c, 0] == row[0] & df.iloc[c, 1] == row[3]):
                            df.iloc[c, 1] = row[3]
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
    
    for index, row in SSdf.iterrows():
        ID = row['Player_IDs'] 
        Level = row['Level'] 
        Year = row['Year']
        paths = setPaths(Level, Year)
        SSdf.at[index, 'Max_Sprint_Speed'] = findMaxSprintSpeed(ID, paths[0], paths[1], paths[2])
    SSdf.to_csv('shortstops.csv', index=False, header=True)

    for index, row in CFdf.iterrows():
        ID = row['Player_IDs'] 
        Level = row['Level'] 
        Year = row['Year']
        paths = setPaths(Level, Year)
        CFdf.at[index, 'Max_Sprint_Speed'] = findMaxSprintSpeed(ID, paths[0], paths[1], paths[2])
    CFdf.to_csv('center_fielders.csv', index=False, header=True)

    for index, row in SSCFdf.iterrows():
        ID = row['Player_IDs'] 
        Level = row['Level'] 
        Year = row['Year']
        paths = setPaths(Level, Year)
        SSCFdf.at[index, 'Max_Sprint_Speed'] = findMaxSprintSpeed(ID, paths[0], paths[1], paths[2])
    SSCFdf.to_csv('shortstop_and_center_fielders.csv', index=False, header=True)

    print("DONE NOW")

if __name__ == "__main__":
    main()