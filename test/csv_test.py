import csv

myData = [["Name", "Age", "Gender"],
          ['Alex', '13', 'M'],
          ['Ripley', '32', 'F']]

with open('example2.csv', 'w',newline='') as f:
    writer = csv.writer(f)
    writer.writerows(myData)