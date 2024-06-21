# Find max sprint speed for each relevant player
# Measured in ft/sec
# For now: only from baserunning
# Adds results to .csv flies

import pandas as pd
import os
import csv

#Set file_paths to your path to the folders within the player_pos folder
file_path_1883_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home1A"
file_path_1883_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home2A"
file_path_1883_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home3A"
file_path_1883_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1883/Home4A"
file_path_1884_1 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home1A"
file_path_1884_2 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home2A"
file_path_1884_3 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home3A"
file_path_1884_4 = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/player_pos/Season_1884/Home4A"

def findMaxSprintSpeed(Player_ID, Level, Year, file_path):
    for root, dirs, files in os.walk(file_path):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        print("hello")
    return(0)

def findRelevantPlays():
    #Set file_path to your path to the game_info folder
    file_path = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info"
    data = {}
    df = pd.DataFrame(data)
    for root, dirs, files in os.walk(file_path):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        if(row[6] == "bottom"):
                            print("hello")
    return(df)

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
        if(Year == 1883):
            if(Level == 1):
                file_path = file_path_1883_1
            elif(Level == 2):
                file_path = file_path_1883_2
            elif(Level == 3):
                file_path = file_path_1883_3
            else:
                file_path = file_path_1883_4
        else:
            if(Level == 1):
                file_path = file_path_1884_1
            elif(Level == 2):
                file_path = file_path_1884_2
            elif(Level == 3):
                file_path = file_path_1884_3
            else:
                file_path = file_path_1884_4
        SSdf.at[index, 'Max_Sprint_Speed'] = findMaxSprintSpeed(ID, Level, Year, file_path)
    SSdf.to_csv('shortstops.csv', index=False, header=True)

    for index, row in CFdf.iterrows():
        ID = row['Player_IDs'] 
        Level = row['Level'] 
        Year = row['Year']
        if(Year == 1883):
            if(Level == 1):
                file_path = file_path_1883_1
            elif(Level == 2):
                file_path = file_path_1883_2
            elif(Level == 3):
                file_path = file_path_1883_3
            else:
                file_path = file_path_1883_4
        else:
            if(Level == 1):
                file_path = file_path_1884_1
            elif(Level == 2):
                file_path = file_path_1884_2
            elif(Level == 3):
                file_path = file_path_1884_3
            else:
                file_path = file_path_1884_4
        CFdf.at[index, 'Max_Sprint_Speed'] = findMaxSprintSpeed(ID, Level, Year, file_path)
    CFdf.to_csv('center_fielders.csv', index=False, header=True)

    for index, row in SSCFdf.iterrows():
        ID = row['Player_IDs'] 
        Level = row['Level'] 
        Year = row['Year']
        if(Year == 1883):
            if(Level == 1):
                file_path = file_path_1883_1
            elif(Level == 2):
                file_path = file_path_1883_2
            elif(Level == 3):
                file_path = file_path_1883_3
            else:
                file_path = file_path_1883_4
        else:
            if(Level == 1):
                file_path = file_path_1884_1
            elif(Level == 2):
                file_path = file_path_1884_2
            elif(Level == 3):
                file_path = file_path_1884_3
            else:
                file_path = file_path_1884_4
        SSCFdf.at[index, 'Max_Sprint_Speed'] = findMaxSprintSpeed(ID, Level, Year, file_path)
    SSCFdf.to_csv('shortstop_and_center_fielders.csv', index=False, header=True)


if __name__ == "__main__":
    main()