import operator
import math
from flask import render_template, jsonify, request, g
from apps import create_app
# from apps.models import Sequential, Clinical
# from utils import model_to_dict
import pickle
import numpy as np
import pandas as pd

app = create_app()

with open('test/data.pkl', 'rb') as f:
    data = pickle.load(f)
hidden_data = data.copy()
clinical_data = pd.read_csv('./test/clinical data.csv', dtype=str, na_values='')
clinical_data.fillna('', inplace=True)
clinical_data.rename(columns={'Unnamed: 0':'number'}, inplace=True)

hidden_seq = []
start, end, values = 0, 0, 0
SEQ_DATA = list()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_clinical')
def get_clinical():
    number = request.args.get('number', 0)
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    rsp_list = list()
    sample = clinical_data.iloc[int(number), :]
    sample = sample.to_dict()
    rsp_list.append(sample)
    total_page = 1
    return jsonify({'code': 0, 'count': total_page, 'data': rsp_list})


@app.route('/index_data')
def index_data():
    global SEQ_DATA
    # number_list = request.args.get('number_list', 'null')
    number_time = request.args.get('number_time', None)
    page = int(request.args.get('page'))
    limit = int(request.args.get('limit'))
    rsp_list = list()

    if page > 1:
        n_list = SEQ_DATA
        n_data_list = n_list[(page - 1) * limit:page * limit + limit]
        for i in n_data_list:
            sample = clinical_data.iloc[int(i), :]
            sample = sample.to_dict()
            rsp_list.append(sample)
        total_page = len(n_list)
        return jsonify({'code': 0, 'count': total_page, 'data': rsp_list})
    else:
        if SEQ_DATA:
            n_data_list = SEQ_DATA[:limit]
            for i in n_data_list:
                sample = clinical_data.iloc[int(i), :]
                sample = sample.to_dict()
                rsp_list.append(sample)
            total_page = len(SEQ_DATA)
            return jsonify({'code': 0, 'count': total_page, 'data': rsp_list})
        rsp_number = search_in_rest(hidden_data, hidden_seq, int(start), int(end), float(values))
        SEQ_DATA = rsp_number

        for num in rsp_number[:limit]:
            sample = clinical_data.iloc[int(num), :]
            sample = sample.to_dict()
            rsp_list.append(sample)
        total_page = len(rsp_number)
        # print('rsp_list', rsp_list)
    return jsonify({'code': 0, 'count': total_page, 'data': rsp_list})


@app.route('/get_data')
def get_data():
    global start, end, values
    number = request.args.get('number', 0)
    values = request.args.get('values', None)
    start = request.args.get('start', None)
    end = request.args.get('end', None)
    seq_dict = hidden_data[int(number)].tolist()
    try:
        if values:
            values = float(values)
            start = int(start)
            end = int(end)
            if start < 0 or start > 49:
                return jsonify({'msg': 'Please enter the correct parameters'})
            if end < 0 or start > 49:
                return jsonify({'msg': 'Please enter the correct parameters'})
    except:
        return jsonify({'msg': 'Please enter the correct parameters'})

    y_data = list()
    number_list = list()
    for i in range(len(seq_dict)):
        # seq1 = seq_dict[i]
        y_data_dict = dict()
        seq_list = seq_dict[i]
        if values:
            start_list = seq_list[start:end + 1]
            # print(start_list)
            if all(i >= values for i in start_list):
                y_data_dict['type'] = 'line'
                y_data_dict['data'] = seq_list
                # y_data_dict['lineStyle'] = {'emphasis': {'color': '#594837'}}
                y_data_dict['itemStyle'] = {'normal': {'lineStyle': {'color': '#1948F7'}}}
                y_data_dict['markLine'] = {
                    'data': [{'lineStyle': {'type': 'solid', 'color': '#3398DB'}, 'yAxis': values}]}
                y_data.append(y_data_dict)
                number_list.append(i)
            else:
                y_data_dict['type'] = 'line'
                y_data_dict['data'] = seq_list
                y_data_dict['hoverAnimation'] = False
                y_data_dict['itemStyle'] = {'normal': {'lineStyle': {'color': '#808A87'}}}
                y_data.append(y_data_dict)
        else:
            y_data_dict['type'] = 'line'
            y_data_dict['data'] = seq_list
            y_data.append(y_data_dict)
    global hidden_seq
    hidden_seq = number_list
    print(hidden_seq)
    return jsonify({'msg': '0000', 'number': number, 'y_data': y_data, 'number_list': number_list})


def search_in_rest(hidden, number_list, starts, ends, threshold):
    people_list = []
    for i in range(hidden.shape[0]):
        if np.all(hidden[i, number_list, starts:ends + 1] > threshold): people_list.append(i)
    return people_list


if __name__ == '__main__':
    app.run()
