from openpyxl import workbook, load_workbook

if __name__ == '__main__':
    wb = load_workbook("ekyc_new.xlsx")
    ws = wb.active
    ws.delete_cols(1, 1)
    ws.delete_cols(3,2)
    ws.delete_cols(14, 10)
    datas = []
    for row in ws:
        data_row = []
        for cell in row:
            c = cell.value
            if c is None:
                c = ''
            data_row.append(str(c))
        datas.append(tuple(data_row))
        print(data_row)
    datas.pop(0)

