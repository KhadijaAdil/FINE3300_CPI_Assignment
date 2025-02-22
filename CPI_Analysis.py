#Let's start off by importing pandas since we know we'll be needing them
import pandas as pd

#Next, let's create a list of all the provinces we'll be dealing with
provinces = ["AB",
             "BC",
             "Canada",
             "MB",
             "NB",
             "NL",
             "NS",
             "ON",
             "PEI",
             "QC",
             "SK"]

#Now, to create one large data set out of these 11 individual data sets, we must "rearrange" the CPI tables of province and then concatenate them
#However, instead of rearranging each of the individual data sets, we can just create a loop!

#First, we need to create an empty list where all of our new data where go as we extract it from these 11 data sets 
all_new_data = []

#then, we will start off by reading each of the files; we use "index_col = 0" because the first column is the index
for province in provinces:
    df = pd.read_csv(f'{province}.CPI.1810000401.csv', index_col=0)

#next, let's pretend as if we are going through one of the data sets, the new data set we create will come about as we loop through each of the rows and columns
#as we loop through the rows and columns, we have to create a dictionary which stores our each month-item combination and we have to add new "Item", "Month", "Jurisdiction", and "CPI" headers into the new data set
    new_data = []
    for i in range(len(df)):
    #^looping through each of the rows
        for month in df.columns:
        #^looping through each of the columns
            new_data.append({"Item":df.index[i], "Month": month, "Jurisdiction": province, "CPI":df.iloc[i][month]})
            #^creating a dictionary for each month - item combination

    for row in new_data:
        all_new_data.append(row)
        #adding each row of "new_data" to "all_new_data"

#now, we just have a list of dictionaries where each dictionary stored key-value pairs representing a row of data
#thus, we must convert all of these pairs into a structured data frame
df_combined = pd.DataFrame(all_new_data)

#QUESTION 1 ANSWER
print("QUESTION 1 ANSWER")
print(df_combined.head(12))
print("*"*100)

#QUESTION 2 ANSWER
#Average Month to Month Change (food, shelter, all-items excluding food and energy)
df_combined[df_combined["Item"] == "food"]
