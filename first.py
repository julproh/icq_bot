#!/usr/bin/python
# My first program on Python
print ("Hello World!!!")
wb = openpyxl.load_workbook('Questions.xlsx')
sheet = wb.active
#for i in range (1, 4) :
cell = sheet.cell(row=2,column=2)
print(cell.value)

