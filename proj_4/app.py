import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
#################### SQL Alchemy Configuration ##########

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app, db)

########################
##################### Create a Model ##############
class Notes(db.Model):
    __tablename__='notes'
    #num=db.Column(db.Integer, primary_key=True)
    note_name=db.Column(db.Text, primary_key=True)

    def __init__(self, note_name):
        #self.num=num
        self.note_name = note_name
    def __repr__(self):
        return "{}".format(self.note_name)


######################################

@app.route('/')
def index():
   return render_template('index.html')

#notes = []

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method=='POST':
        note_name = request.form.get("note")
        #notes.append(note)
        new_Notes=Notes(note_name)
        db.session.add(new_Notes)
        db.session.commit()
    return render_template("add.html")

@app.route('/search')
def search():
    note_name=request.args.get("note")
    note=Notes.query.filter_by(note_name=note_name).first()
    return render_template("search.html", note=note)

@app.route('/display')
def display_all():
    notes = Notes.query.all()
    return render_template("display.html",notes=notes)

######################################################
if __name__ == '__main__':
    app.run(debug=True)