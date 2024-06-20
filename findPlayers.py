import pandas as pd
import csv
import os

#Finds all unique players (by ID) and puts them into table with format: player_id, level, SS?, CF?, Year
#The same player may have different entries at different levels and/or different years
#SS and CF bools will all be false for now
#Level: 4 = AAA, 3 = AA, 2 = A+, 1 = A-
def findUniquePlayers(file_path):
    data = {'Player_IDs': [],'Level': [],'SS': [],'CF': [], 'Year': [],}
    df = pd.DataFrame(data)

    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            ID = row[1]
            Level = row[0][4:5]
            Year = row[2]
            row_to_check = {'Player_IDs': ID,'Level': Level,'SS': False,'CF': False, 'Year': Year}
            row_df = pd.DataFrame([row_to_check])
            #Check if there is any row that satisfies all conditions
            if(not(df == row_df.iloc[0]).all(axis=1).any()):
                new_row = {'Player_IDs': ID,'Level': Level,'SS': False,'CF': False,'Year': Year}
                new_row_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_row_df], ignore_index=True)
    df.iloc[0, df.columns.get_loc('SS')] = False
    df.iloc[0, df.columns.get_loc('CF')] = False
    return(df)

#fills in which players have played SS/CF
def fillPositions(file_path, df):
    for root, dirs, files in os.walk(file_path):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)
                    for row in csv_reader:
                        if(row[6] == "top"):
                            SS = row[12]
                            if(not(SS) == "NA"):
                                condition = (df['Player_IDs'] == SS) & (df['Year'] == row[0][0:4]) & (df['Level'] == row[1][4:5])
                                if(df.loc[condition].empty): #there are some errors in the data that cause this to happen
                                    print("No matching rows found.") 
                                    #print(SS)
                                    #print(row[0])
                                else:
                                    df.loc[condition, 'SS'] = True
                            CF = row[14]
                            if(not(CF) == "NA"):
                                condition = (df['Player_IDs'] == CF) & (df['Year'] == row[0][0:4]) & (df['Level'] == row[1][4:5])
                                if(df.loc[condition].empty):
                                    print("No matching rows found.")
                                    #print(CF)
                                    #print(row[0])
                                else:
                                    df.loc[condition, 'CF'] = True
    return(df)

                        

def main():
    #set file_path to your path to team_info.csv 
    file_path = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/team_info.csv"
    df = findUniquePlayers(file_path)

    #iterate through all game_info files to find players that played SS/CF
    #set file_path to your path to the game_info folder
    file_path = "C:/Users/samdo/OneDrive/Desktop/SMT_2024/2024_SMT_Data_Challenge/2024_SMT_Data_Challenge/game_info"
    fillPositions(file_path, df)

    #sort table into 3 separtate tables: SS table, CF table, Both table
    SSdata = {'Player_IDs': [],'Level': [],'Year': []}
    SSdf = pd.DataFrame(SSdata)

    CFdata = {'Player_IDs': [],'Level': [],'Year': []}
    CFdf = pd.DataFrame(CFdata)

    SSCFdata = {'Player_IDs': [],'Level': [],'Year': []}
    SSCFdf = pd.DataFrame(SSCFdata)

    for index, row in df.iterrows():
        if(row["SS"]):
            if(row["CF"]):
                new_row = {'Player_IDs': row["Player_IDs"],'Level': row["Level"],'Year': row["Year"]}
                new_row_df = pd.DataFrame([new_row])
                SSCFdf = pd.concat([SSCFdf, new_row_df], ignore_index=True)
            else:
                new_row = {'Player_IDs': row["Player_IDs"],'Level': row["Level"],'Year': row["Year"]}
                new_row_df = pd.DataFrame([new_row])
                SSdf = pd.concat([SSdf, new_row_df], ignore_index=True)
        elif(row["CF"]):
            new_row = {'Player_IDs': row["Player_IDs"],'Level': row["Level"],'Year': row["Year"]}
            new_row_df = pd.DataFrame([new_row])
            CFdf = pd.concat([CFdf, new_row_df], ignore_index=True)
    
    #print(SSdf)
    SSdf.to_csv('shortstops.csv', index=False, header=True)
    #print(CFdf)
    CFdf.to_csv('center_fielders.csv', index=False, header=True)
    #print(SSCFdf)
    SSCFdf.to_csv('shortstop_and_center_fielders.csv', index=False, header=True)



if __name__ == "__main__":
    main()