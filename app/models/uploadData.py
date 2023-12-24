from app import db

# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired

class UploadData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    data = db.Column(db.LargeBinary)

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __str__(self):
        return f""

# class UploadDataForm(FlaskForm):
#     # tanggal = StringField('Tanggal', validators=[DataRequired()])
#     label = StringField('Label', validators=[DataRequired()])
#     Tweet = StringField('Tweet', validators=[DataRequired()])
#     submit = SubmitField('Simpan')

