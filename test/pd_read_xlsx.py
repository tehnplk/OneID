import pandas as pd

# Read the Excel file into a pandas DataFrame
df = pd.read_excel("ekyc_new.xlsx")

# Drop the column(s) you want to remove
df.drop(['ผู้อำนวยการ', 'เจ้าหน้าที่ HR.'], axis=1, inplace=True)

# Save the modified DataFrame back to an Excel file
df.to_excel("output.xlsx", index=False)
