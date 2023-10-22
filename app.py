from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)

def __repr__(self):
    return '<Person %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update/', methods=['GET', 'POST'])
def addPerson():
    return render_template('addperson.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)