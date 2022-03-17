#1.	Print the name of your class
print("Group 3")
#2.	Print your full name
print("Roy Dijkstra")
#3.	Print the name of the file involved
print("File_A_group3.csv")

#4.	Read in the file with a line of code, no wizards are allowed
import pandas as pd

df = pd.read_csv("week4Test\\File_A_group3.csv", sep=";")

#5.	Drop all columns from the dataframe except for
dfNewAddresses = df[['CDR_ID', 'Start_datetime', 'End_datetime', 'Contract_ID', 'Volume', 'Charge_Point_Address', 'Charge_Point_ZIP']]

#6.	All the values in the column Contract_ID contain  “-” remove these.
dfNewAddresses = dfNewAddresses.drop(dfNewAddresses[dfNewAddresses.Contract_ID.str.contains("-", na=True, regex = False)].index)

#7.	Rename all columns in such a way that  no prefix “Charge_Point_” appear
renamedAddressCols = dfNewAddresses.rename(columns={'Charge_Point_Address': 'Address', 'Charge_Point_ZIP': 'ZIP'})

#8.	Create a new dataframe called dfFilter containing only observations for Volume>0.0
renamedAddressCols['Volume'] = renamedAddressCols['Volume'].str.replace(",", ".").astype(float)
dfFilter = renamedAddressCols.drop(renamedAddressCols[renamedAddressCols.Volume <= 0.0].index)

#9.	Count the number of sessions ( = volume) for each Address
dfFilter['Address'].value_counts()

#10. Add an extra column for a VolumeType
dfFilter['VolumeType'] = dfFilter['Volume'].apply(lambda x: "High" if x > 10 else "Low")







