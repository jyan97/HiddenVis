# -*- coding: utf-8 -*-
# @Time    : 2020/8/23 0023 13:24
import csv
t = list()
with open('x_axis.csv','r') as f:
    d = csv.reader(f)
    for i in d:
        t.append(i[0])
print(t)