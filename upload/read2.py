import pandas as pd

# Specify the path to your Excel file
file_path = 'ekyc_hospital_summary_090136.xlsx'

columns_to_read = [
    'รหัส',
    'ชื่อหน่วยให้บริการ',
    'เขตสุขภาพ',
    'จังหวัด',
    'อำเภอ',
    'ตำบล',
    'จำนวนอุปกรณ์',
    'จำนวน KYC (คน)',
    #'จำนวน Token (คน)',
    'จำนวน Token (ครั้ง)',
    'จำนวนยืนยัน Token (คน)',
    'จำนวนบุคลากร',
    'จำนวนบุคลากร ยืนยัน eKYC',
    '% บุคลากร eKYC'
]

# Read the specific columns from the Excel file
df = pd.read_excel(file_path, usecols=columns_to_read)
df = df[df['จังหวัด'] == 'พิษณุโลก']
df = df.fillna('')
df['รหัส'] = df['รหัส'].astype(str)
df['รหัส'] = df['รหัส'].str.zfill(5)

# Display the DataFrame
#list_of_tuples = [tuple(row) for row in df.to_records(index=False)]
list_of_tuples = list(df.itertuples(index=False, name=None))
print(list_of_tuples)
print(len(list_of_tuples))
