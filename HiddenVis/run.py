from flask import render_template, jsonify, request, g, redirect, url_for
from apps import create_app
import pickle
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
import os
import matplotlib.pyplot as plt
import random
from pyecharts.charts import Sankey
from pyecharts import options as opts

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
date = ['Mon3:40', 'Mon7:00', 'Mon10:20', 'Mon13:40', 'Mon17:00','Mon20:20', 'Mon23:40', 'Tue3:00', 'Tue6:20', 'Tue9:40',
        'Tue13:00', 'Tue16:20', 'Tue19:40', 'Tue23:00','Wed2:20', 'Wed5:40', 'Wed9:00', 'Wed12:20',
        'Wed15:40', 'Wed19:00', 'Wed22:20', 'Thu1:40','Thu5:00', 'Thu8:20', 'Thu11:40', 'Thu15:00',
        'Thu18:20', 'Thu21:40', 'Fri1:00', 'Fri4:20','Fri7:40', 'Fri11:00', 'Fri14:20', 'Fri17:40',
        'Fri21:00', 'Sat0:20', 'Sat3:40', 'Sat7:00','Sat10:20', 'Sat13:40', 'Sat17:00', 'Sat20:20',
        'Sat23:40', 'Sun3:00', 'Sun6:20', 'Sun9:40','Sun13:00', 'Sun16:20', 'Sun19:40', 'Sun23:00']




@app.route('/redi_upload')
def redi_upload():
    return render_template('index.html')

@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, r'test\data.pkl')
        f.save(upload_path)
        return redirect(url_for('upload'))
    return render_template('upload.html')

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
    return jsonify({'msg': '0000', 'number': number, 'y_data': y_data, 'number_list': number_list})


def search_in_rest(hidden, number_list, starts, ends, threshold):
    people_list = []
    for i in range(hidden.shape[0]):
        if np.all(hidden[i, number_list, starts:ends + 1] > threshold): people_list.append(i)
    return people_list



@app.route("/read")
def read_csv():
    df = pd.read_csv("test/clinical data.csv")
    columns = list(df.columns)
    return render_template('index.html', columns=columns)


@app.route("/plot/<pk>/<size>")
def plot(pk, size):
    df = pd.read_csv("test/clinical data.csv")
    df = df[pk]
    if df.dtype == "float64" or df.dtype == "int64":
        minValue = df.min()
        maxValue = df.max()
        list1 = []
        label = []
        minNowValue = None
        for i in range(int(minValue), int(maxValue) + int(size), int(size)):
            list1.append(i)
            if minNowValue is not None:
                label.append(str(minNowValue) + "-" + str(i))

            minNowValue = i
        a = pd.cut(df, list1, labels=label)
        df = pd.Series(a, name=pk)

        # 统计类别
    count = df.value_counts()
    count = count.sort_index(axis=0, ascending=True)
    name = str(random.randint(0, 1000000))
    plt.bar(count.index, count)
    plt.savefig("./apps/static/images/" + name + '.jpg')
    plt.clf()


    df = pd.read_csv("test/clinical data.csv")
    df = df.iloc[SEQ_DATA, :]
    df = df[pk]
    if df.dtype == "float64" or df.dtype == "int64":
        minValue = df.min()
        maxValue = df.max()
        list1 = []
        label = []
        minNowValue = None
        for i in range(int(minValue), int(maxValue) + int(size), int(size)):
            list1.append(i)
            if minNowValue is not None:
                label.append(str(minNowValue) + "-" + str(i))

            minNowValue = i
        a = pd.cut(df, list1, labels=label)
        df = pd.Series(a, name=pk)

        # 统计类别
    count = df.value_counts()
    count = count.sort_index(axis=0, ascending=True)
    plt.bar(count.index, count)
    plt.savefig("./apps/static/images/" + name + '.png')
    plt.clf()
    return name

def group_stack(df):
  filter_col = [col for col in df if col.startswith('MIN')]
  activity = df[filter_col]
  activity = activity.stack().tolist()
  activity = pd.Series(activity)
  return activity.to_frame().T

def sankey_preprocess(df, duration):
  df = df.dropna(axis=0).copy()
  df['mort'] = df['mort'].map({1:'death', 0:'alive'})
  for i in range(len(duration)):
    start_time = 0 if duration[i][0]==0 else 220+(duration[i][0]-1)*200
    end_time = 220+200*duration[i][1]
    threshold = df.iloc[:,2+start_time:2+end_time].mean(axis=1).mean()
    temp = np.where(df.iloc[:,2+start_time:2+end_time].mean(axis=1) >= threshold, str(date[duration[i][0]-1])+'_Active_', str(date[duration[i][0]-1])+'_NonActive_')
    df['active_mort'+str(i)] = temp + df['mort']
    # df[str(date[duration[i][0]-1])+'to'+str(date[duration[i][1]])] = np.where(df.iloc[:,2+start_time:2+end_time].mean(axis=1) >= threshold, str(date[duration[i][0]-1])+'_Active', str(date[duration[i][0]-1])+'_NonActive')
  return df

@app.route('/sankey', methods=['GET', 'POST'])
def sankey():
    if request.method == "POST":
        duration_list = request.form['interval']
        duration_list = eval(duration_list)
        ###
        clinical = pd.read_csv("test/clinical data.csv", index_col=0)
        act_analysis = pd.read_csv('act_analysis.csv', index_col=0)
        act_analysis.reset_index(inplace=True)
        filter_col = [col for col in act_analysis if col.startswith('MIN')]
        activity = act_analysis[['WEEKDAY', 'SEQN'] + filter_col]

        days_act = activity[activity.SEQN != 34743]
        days_act = days_act.sort_values(['SEQN', 'WEEKDAY'], ascending=True).groupby(['SEQN']).apply(group_stack)
        days_act.reset_index(inplace=True)
        days_act = days_act.drop(columns='level_1')
        days_act.columns = ['SEQN'] + [str(i) for i in range(1440 * 7)]
        days_act = pd.concat([clinical.mort, days_act], axis=1)

        sankey_1 = sankey_preprocess(days_act, duration_list)
        sankey = sankey_1.iloc[:, -len(duration_list):].copy()

        nodes = []

        for i in range(sankey.shape[1]):
            values = sankey.iloc[:, i].unique()
            for value in values:
                dic = {}
                dic['name'] = value
                nodes.append(dic)

        first = sankey.groupby([sankey.columns[0], sankey.columns[1]]).size().reset_index(name='counts')
        second = sankey.groupby([sankey.columns[1], sankey.columns[2]]).size().reset_index(name='counts')
        third = sankey.groupby([sankey.columns[2], sankey.columns[3]]).size().reset_index(name='counts')
        second.columns = first.columns
        third.columns = first.columns
        result = pd.concat([first, second, third], axis=0, ignore_index=True)

        linkes = []
        for i in result.values:
            dic = {}
            dic['source'] = i[0]
            dic['target'] = i[1]
            dic['value'] = i[2]
            linkes.append(dic)

        pic = (
            Sankey()
                .add('Activity and Non_Activity',
                     nodes,
                     linkes,
                     linestyle_opt=opts.LineStyleOpts(opacity=0.5, curve=0.5, color="source"),
                     label_opts=opts.LabelOpts(position="right"),
                     node_gap=5,
                     )
        )
        pic.render('apps/templates/sankey.html')

        return redirect(url_for('sankey'))
    return render_template('sankey.html')


if __name__ == '__main__':
    app.run()
