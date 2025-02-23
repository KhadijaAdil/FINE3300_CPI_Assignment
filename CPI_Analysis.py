#BASE MODEL
#Let's start off by importing pandas since we know we'll be needing them
import pandas as pd

#Next, let's create a list of all the provinces we'll be dealing with
provinces = ["Canada",
             "AB",
             "BC",
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

#now, let's sort the data so that its filtered by to show all the item values by month (I want "January") and by province (I want "AB")

#************************************************************************************************************************************************************************************************************************************************
#QUESTION 1 ANSWER
print(" ")
print("QUESTION 1 ANSWER:")
print("THE FIRST 12 ROWS OF MY DATA FRAME")
print(" ")
print(df_combined.head(12))
print(" ")

print("OR IF WE WANT TO SEE THE FIRST 12 ROWS FOR JUST CANADA'S JANUARY CPI DATA AS PER THE TABLE IN THE ASSIGNMENT")
print(" ")
df_combined_filtered = pd.concat([df_combined[(df_combined["Jurisdiction"] == "Canada") & (df_combined["Month"] == "24-Jan")], df_combined[~((df_combined["Jurisdiction"] == "Canada") & (df_combined["Month"] == "24-Jan"))]])
print(df_combined_filtered.head(12))
#Please note, I am using the "~" and concatenate function because I still want to include all the rows that do not have "Canada" & "24-Jan"
print("*"*100)

#************************************************************************************************************************************************************************************************************************************************

#QUESTION 2 ANSWER
#We need to find the average month-to-month change in food, shelter, and all-items excluding food and energy
#Thus, we have four broad steps:
# 1. We need to filter our data frame for these specific items
# 2. Then we need to number each of the months
# 3. Then we need to find the average month to month % change for each item for each province
# 4. Finally, we can calculate the average %change for each item

#first, lets filter for our three items
df_filtered_1 = df_combined[df_combined["Item"].isin(["Food", "Shelter", "All-items excluding food and energy"])].copy()
#next, we must create a dictionary which maps our month names to numbers
month_order = {"24-Jan":1, "24-Feb":2, "24-Mar":3, "24-Apr":4, "24-May":5, "24-Jun":6, "24-Jul":7, "24-Aug":8, "24-Sep":9, "24-Oct":10, "24-Nov":11, "24-Dec":12}
df_filtered_1["Month_Num"] = df_filtered_1["Month"].map(month_order)
#so now we have add a new column to df_filtered_1 which has a number for each month
df_filtered_1 = df_filtered_1.sort_values(by=["Jurisdiction","Item","Month_Num"])
#we have now filtered out data first by jurisdiction and then by item and finally by the numerical month value
df_filtered_1["Pct_change"] = df_filtered_1.groupby(["Jurisdiction","Item"])["CPI"].pct_change()*100
#now we have calculated the percentage change for each jurisdiction and item 
avg_pct_change = df_filtered_1.groupby(["Jurisdiction", "Item"])["Pct_change"].mean().round(1)
avg_pct_change_1 = avg_pct_change.round(1).astype(str)+"%"
#finally, we can calculate the average percertage change for each item across all jurisdictions
print(" ")
print("QUESTION 2 ANSWER:")
print(" ")
print("THE AVERAGE MONTH-TO-MONTH % CHANGE ACROSS THE FOLLOWING ITEMS, IN EACH JURISDICTION IS AS FOLLOWS:")
print(avg_pct_change_1)
print("*"*100)

#************************************************************************************************************************************************************************************************************************************************

#QUESTION 3 ANSWER
#to calculate the highest average change in each of the categories
avg_pct_change_per_jur = df_filtered_1.groupby(["Item", "Jurisdiction"])["Pct_change"].mean()
highest_change_per_item = avg_pct_change_per_jur.groupby("Item").idxmax()
jurisdiction_names = []
for item, jurisdiction in highest_change_per_item:
    jurisdiction_names.append(jurisdiction)
highest_change_values = avg_pct_change_per_jur.groupby("Item").max()
formatted_pct_chg = []
for value in highest_change_values:
    formatted_pct_chg.append(f"{value:.1f}%")
highest_change_jurisdiction_item = pd.DataFrame ({"Item":highest_change_per_item.index, " Jurisdiction With Highest Change": jurisdiction_names, " Highest Avg % Change" : formatted_pct_chg})
print(" ")
print("QUESTION 3 ANSWER:")
print(" ")
print("THE PROVINCES WHICH HAD THE HIGHEST AVERAGE CHANGE ACROSS EACH OF THE THREE CATEGORIES ARE:")
print(" ")
print(highest_change_jurisdiction_item)
print("*"*100)

#************************************************************************************************************************************************************************************************************************************************

#QUESTION 4 ANSWER
#to find the annual change in CPI for serviced across Canada and all provinces we have to follow 5 general steps
#first, we must filter for services from the dataset
#second, we must get the January and December prices for each store
#third, we must calculate the annual percetage change by calculating [(dec price - jan prices)/jan prices]
#then, we'll seperate out Canada's change and average the change for all the provinces
#finally we'll create a table to show our results!

#first, filter for services
df_services = df_combined[df_combined["Item"] == "Services"]
#then, we'll get Jan and Dec CPI per province
jan_prices = df_services[df_services["Month"] == "24-Jan"].set_index("Jurisdiction")["CPI"]
dec_prices = df_services[df_services["Month"] == "24-Dec"].set_index("Jurisdiction")["CPI"]
#next, we'll calculate the annual percentage change
annual_change_per_jurisdiction = ((dec_prices - jan_prices) / jan_prices) * 100
#next, we'll extract canada's change and calculate the average for all the provinces
canada_change = annual_change_per_jurisdiction["Canada"]
provincial_change = annual_change_per_jurisdiction.drop("Canada").mean()
#some quick formatting to make sure everything looks presentable
canada_change = f"{canada_change.round(1)}%"
provincial_change = f"{provincial_change.round(1)}%"
#now, let's generate our data frame
annual_change = pd.DataFrame({"Jurisdiction":["Canada", "All Provinces"], " Annual Change (%)": [canada_change, provincial_change]})
print(" ")
print("QUESTION 4 ANSWER:")
print(" ")
print("THE ANNUAL CHANGE IN CPI FOR SERVICES ACROSS CANADA AND ALL PROVINCES IS AS FOLLOWS:")
print(" ")
print(annual_change)
print("*"*100)

#************************************************************************************************************************************************************************************************************************************************

#QUESTION 5 ANSWER
#we must now find the region with the highest inflation in services
highest_inflation_jurisdiction = annual_change_per_jurisdiction.idxmax()
highest_inflation_value = annual_change_per_jurisdiction.max()
highest_inflation_value = f"{highest_inflation_value:.1f}%"
#our final data frame!
highest_inflation_services = pd.DataFrame({"Jurisdiction":[highest_inflation_jurisdiction], " Annual Services Inflation": [highest_inflation_value]})
print(" ")
print("QUESTION 5 ANSWER:")
print(" ")
print("THE JURISDICTION WITH THE HIGHEST INFLATION IN SERVICES IS:")
print(" ")
print(highest_inflation_services)
print("*"*100)
