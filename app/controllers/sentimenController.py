import os
from flask import Flask, request, flash, render_template, jsonify, json
from app.controllers.function import preprocess_data, result_nb
import pandas
import app
from flask_marshmallow import Marshmallow
from app.models.tesModel import db, TesModel

ma = Marshmallow(app)


class TesModelSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Tweet', 'label', 'tes')

# init schema
tesModel_schema = TesModelSchema()
tesModels_schema = TesModelSchema(many=True)


labels = [
  'POSITIF', 'NEGATIF', 'NETRAL'
]

colors = [
  '#1cc88a', '#e74a3b', '#f6c23e'
]

def klasifikasi():
    # text = pandas.read_csv('app/uploads/datauji.csv', encoding='latin-1')
    text = TesModel.query.with_entities(TesModel.Tweet, TesModel.label).all()
    tableData = pandas.DataFrame(text, columns=['Tweet', 'label'])
    tableData['label'] = tableData['label']

    accuracy_nv, y_test = result_nb(tableData)
    accuracy_nv = (round(accuracy_nv, 3) * 100)
    
    y_test = y_test.reset_index()
    positif, negatif, netral = y_test['label'].value_counts()
    total = positif + negatif + netral
    # print(y_test['label'].value_counts() )

    pie_labels = labels
    pie_colors = colors
    pie_values = [positif, negatif, netral]

    bar_labels = labels
    bar_values = [positif, negatif, netral]
    
    return render_template ('klasifikasinv.html', tweet_positive = positif, tweet_negative = negatif, 
                            tweet_netral = netral, total_tweet = total, accuracy_nv = accuracy_nv, 
                            labels = pie_labels, colors = pie_colors, values = pie_values, 
                            bar_labels = bar_labels, bar_values = bar_values, 
                            tables=[tableData.to_html(classes='table table-bordered', table_id='dataTable')])