from app import app
from flask import request, jsonify, render_template, redirect
from flask_marshmallow import Marshmallow
from app.models.tesModel import db, TesModel
from app.controllers.function import preprocess_data
import pandas as pd
import pickle
import os

ma = Marshmallow(app)

class TesModelSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Tweet', 'label', 'tes')


# init schema
# init schema
tesModel_schema = TesModelSchema()
tesModels_schema = TesModelSchema(many=True)

def uploadData():
  model = pickle.load(open('app/uploads/sentiment1.pkl','rb'))
  # model = joblib.load("twitter_sentiment.pkl")
  vectorizer = pickle.load(open('app/uploads/vector1.pkl','rb'))

  file = request.files['file']
  
  df = pd.read_csv(file)
  print(df.head())
  tweet = df['Tweet']
  newTesModels = []

  for i in tweet:
     hasilprepro = preprocess_data(i)
     hasiltfidf = vectorizer.transform([hasilprepro])
     nb = ''
     hasilnb = model.predict(hasiltfidf)
     if hasilnb == 0:
       nb = 'netral'
     elif hasilnb == 1:
       nb = 'negatif'
     else:
       nb = 'positif'
     newTesModel = TesModel(i, nb, 'false')
     db.session.add(newTesModel)  # Menambahkan newTesModel ke sesi database
     newTesModels.append(newTesModel)
  db.session.commit()  # Menyimpan perubahan dalam sesi database

  tesModel_data = []

  for tesModel in newTesModels:
    tesModel_data.append({
        'Tweet': tesModel.Tweet,
        'label': tesModel.label,
        'tes': tesModel.tes
    })

  # Membuat DataFrame dari data TesModel
  # df_tesModel = pd.DataFrame(tesModel_data)

# Menampilkan DataFrame sebagai tabel
  # print(df_tesModel)
  file.save(os.path.join('app/uploads/', 'databaru.csv'))  
  return render_template ('tambahDataAdmin.html',newTesModels=newTesModels)

# def getAllUploadData():
#     allUploadData = UploadData.query.order_by(UploadData.id).all()
#     result = uploadDatas_schema.dump(allUploadData)
#     return jsonify({"msg": "Success Get all data", "status": 200, "data": result})
