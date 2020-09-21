# -*- coding: utf-8 -*-
# @Time    : 2020/8/19 0019 20:16

import pickle
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="password",
    database="flask_echarts"
)
mycursor = mydb.cursor()
sql = "INSERT INTO sequential(number, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12" \
      ", value13, value14, value15, value16, value17, value18, value19, value20, value21, value22, value23, value24, value25, value26" \
      ", value27, value28, value29, value30, value31, value32, value33, value34, value35, value36, value37, value38, value39, value40" \
      ", value41, value42, value43, value44, value45, value46, value47, value48, value49, value50)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
      ", %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" \
      ", %s, %s, %s, %s, %s, %s, %s)"


def insert(val):
    mycursor.execute(sql, val)


with open('data.pkl','rb') as f:
    data = pickle.load(f)
    i = 0
    for data1 in data:
        print(i)
        for data2 in data1:
            t1 = [i]
            t2 = list(map(float,data2))
            t = t1 + t2
            t_data = tuple(t)
            insert(t_data)
        i += 1
mydb.commit()
