from app import app
from flask import request, jsonify, render_template, redirect, Response
from flask_marshmallow import Marshmallow
from app.models.tesModel import db, TesModel
from app.controllers.function import preprocess_data
# from app.controllers.coba import preprocess_data, tfidf_transformer, bow_transformer
import pickle
import csv
import io
import joblib

ma = Marshmallow(app)

class TesModelSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Tweet', 'label', 'tes')

# init schema
tesModel_schema = TesModelSchema()
tesModels_schema = TesModelSchema(many=True)


def addTesModel():
    tweet = request.form['Tweet']
    label = request.form['label']

    newTesModel = TesModel(tweet, label)
    db.session.add(newTesModel)
    db.session.commit()
    tesModel = tesModel_schema.dump(newTesModel)
    return jsonify({"msg": "Success add data", "status": 200, "data": tesModel})

def getAllTesModel():
    allTesModel = TesModel.query.order_by(TesModel.id.desc()).all()
    # result = tesModels_schema.dump(allTesModel)
    # result.reverse()
    allTesModel.reverse()
    return jsonify({"msg": "Success Get all data", "status": 200, "data": allTesModel})

def tesmodel():
  # Loading model to compare the results
  model = pickle.load(open('app/uploads/model/sentiment1.pkl','rb'))
  vectorizer = pickle.load(open('app/uploads/model/vector1.pkl','rb'))

  text = request.form['Tweet']
  original_text = request.form['Tweet']

  hasilprepro = preprocess_data(text)
  hasiltfidf = vectorizer.transform([hasilprepro])
  
  # cek prediksi dari kalimat
  nb = ''
  hasilnb = model.predict(hasiltfidf)
  if hasilnb == 0:
    nb = 'netral'
  elif hasilnb == 1:
    nb = 'negatif'
  else:
    nb = 'positif'

  tes = 'true'

  newTesModel = TesModel(text, nb, tes)
  db.session.add(newTesModel)
  db.session.commit()
  return render_template ('tesmodel.html', original_text=original_text, hasilprepro=hasilprepro, hasilnb=nb)

def tesmodelAdmin():
  # Loading model to compare the results
  model = pickle.load(open('app/uploads/model/sentiment1.pkl','rb'))
  vectorizer = pickle.load(open('app/uploads/model/vector1.pkl','rb'))

  text = request.form['tweet']
  original_text = request.form['tweet']

  hasilprepro = preprocess_data(text)
  hasiltfidf = vectorizer.transform([hasilprepro])

  # cek prediksi dari kalimat
  nb = ''
  hasilnb = model.predict(hasiltfidf)
  if hasilnb == 0:
    nb = 'netral'
  elif hasilnb == 1:
    nb = 'negatif'
  else:
    nb = 'positif'

  tes = 'true'
  newTesModel = TesModel(text, nb, tes)
  db.session.add(newTesModel)
  tesModel = TesModel.query.with_entities(TesModel.id, TesModel.Tweet, TesModel.label).filter(TesModel.tes == 'true')
  table = tesModels_schema.dump(tesModel)
  db.session.commit()
  return render_template ('tesmodelAdmin.html', original_text=original_text, hasilprepro=hasilprepro, hasilnb=nb, tables=table)

def getTesModelAdmin():
   tesModel = TesModel.query.with_entities(TesModel.id, TesModel.Tweet, TesModel.label).filter(TesModel.tes == 'true')
   table = tesModels_schema.dump(tesModel)
   return render_template('tesmodelAdmin.html', tables=table)

def exportToCSV():
    # Query data from the database
    data = TesModel.query.with_entities(TesModel.id, TesModel.Tweet, TesModel.label).filter(TesModel.tes == 'true')
  
    # Define the CSV file name
    csv_file = 'data.csv'

    # Create a StringIO object to hold the CSV data
    csv_data = io.StringIO()

    # Write data to the StringIO object
    writer = csv.writer(csv_data)
    writer.writerow(['id', 'Tweet', 'label'])  # Write header row

    for row in data:
        writer.writerow([row.id, row.Tweet, row.label])

    # Prepare the response as a CSV file download
    response = Response(csv_data.getvalue(), mimetype='text/csv')
    response.headers.set('Content-Disposition', f'attachment; filename={csv_file}')

    return response
   
   

