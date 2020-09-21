# -*- coding: utf-8 -*-
# @Time    : 2020/8/22 0022 15:23
import csv
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="password",
    database="flask_echarts"
)
mycursor = mydb.cursor()


with open('clinical data.csv', 'r') as f:
    data = csv.reader(f)
    j = 0
    for i in data:
        if j == 0:
            j += 1
            continue
        else:
            sql = 'insert into clinical values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' \
                  ',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(sql, tuple(i))
    j += 1
mydb.commit()
