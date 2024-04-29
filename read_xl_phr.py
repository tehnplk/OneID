from openpyxl import  workbook,load_workbook

if __name__ == '__main__':
    wb = load_workbook("./xls/phr.xlsx")
    ws = wb.active

    i = 0

    for row in ws:
        cells = []
        for c in row:
            val = str(c.value).replace('\n','')

            cells.append(val)
        print(cells)


