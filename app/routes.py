from app import app
import config
import os
from flask import request, render_template, flash, redirect, url_for, session, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers import userController, tesModelController, analisisController, sentimenAdminController
from app.controllers.userController import Users
from app.models.tesModel import db, TesModel, TesModelForm
# from app.models.uploadData import db, UploadData, UploadDataForm

DATA_PATH = config.DATA_PATH

@app.route('/user', methods=['GET', 'PUT'])
@jwt_required()
def userDetails():
    current_user = get_jwt_identity()
    if(request.method == 'GET'):
        return userController.getDetailUser(current_user)
    if(request.method == 'PUT'):
        return userController.updateUser(current_user)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method == 'GET'):
        return render_template('login.html')
    elif(request.method == 'POST'):
        session.pop('logged_in', None)
        return userController.signIn()

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if (request.method=='GET'):
        return render_template('register.html')
    else:
        return userController.signUp()

@app.route('/', methods=['GET', 'POST'])
def tesmodel():
    if session.get('logged_in') :
         if(request.method == 'GET'):
            return render_template('tesmodel.html')
         elif(request.method == 'POST'):
            return tesModelController.addTesModel()
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)
    
@app.route('/tesmodel/result', methods=['GET', 'POST'])
def tesmodelResult():
    if session.get('logged_in') :
        return tesModelController.tesmodel()
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)
    
@app.route('/sentimen', methods=['GET','POST'])
def sentimenResult():
    if session.get('logged_in') :
        if (request.method=='GET'):
            return render_template ('klasifikasinv.html')
        else:
            return analisisController.klasifikasi()
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)
    
@app.route('/sentimenAdmin/result', methods=['GET','POST'])
def sentimenAdminResult():
    if session.get('logged_in') :
        return sentimenAdminController.klasifikasi()
        # return render_template('klasifikasiAdmin.html')
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)

@app.route('/homeAdmin', methods=['GET'])
def homeAdmin():
    if session.get('logged_in') :
        return render_template('homeAdmin.html')
    else :
        error = "Anda Belum Login"
        return render_template('login-admin.html', error=error)
    
@app.route('/kelolauser', methods=['GET'])
def kelolauser():
    if session.get('logged_in'):
        roles = db.session.query(Users.role).distinct().all()
        return userController.getAllUser()
    else:
        error = "Anda Belum Login"
        return render_template('login.html', error=error)

@app.route('/kelolauser/result', methods=['GET','POST'])
def tambahuser():
    if session.get('logged_in'):
        return userController.tambahUser()
    else:
        error = "Anda Belum Login"
        return render_template('login.html', error=error)
    
@app.route('/tesmodelAdmin', methods=['GET'])
def tesmodelAdmin():
    if session.get('logged_in') :
        return tesModelController.getTesModelAdmin()
    else :
        error = "Anda Belum Login"
        return render_template('login-admin.html', error=error)

@app.route('/tesmodelAdmin/result', methods=['GET', 'POST'])
def tesmodeAdminlResult():
    if session.get('logged_in') :
        return tesModelController.tesmodelAdmin()
    else :
        error = "Anda Belum Login"
        return render_template('login.html', error=error)

@app.route('/editTesModel/<id>', methods=['GET', 'POST'])
def editTesModel(id):
        tes_model = TesModel.query.get_or_404(id)
        form = TesModelForm(obj=tes_model)
        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(tes_model)
            db.session.commit()
            flash('Tes Model updated successfully!', 'success')
            return redirect(url_for('tesmodelAdmin'))  
        return render_template('editTesModel.html', form=form, tes_model=tes_model)  

# @app.route('/hapustesmodel/<tweet>', methods=['GET', 'POST'])
# def hapustesmodel(tweet):
#     # try:
#         tes_model = TesModel.query.filter_by(tweet=tweet).first()
#         # if tes_model:
#         db.session.delete(tes_model)
#         db.session.commit()
#         flash('Berhasil Dihapus!')
#         return redirect(url_for('tesmodelAdmin'))



@app.route('/hapususer/<username>', methods=['GET', 'POST'])
def hapususer(username):
    # try:
        user = Users.query.filter_by(username=username).first()
        # if tes_model:
        db.session.delete(user)
        db.session.commit()
        flash('Berhasil Dihapus!')
        return redirect(url_for('kelolauser'))

@app.route("/exportCSV", methods=['GET'])
def exportCSV():
    return tesModelController.exportToCSV()

@app.route("/download", methods=['GET'])
def download():
    return analisisController.download()
