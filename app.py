from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addPersonBtn/', methods=['GET', 'POST'])
def addPersonBtn():
    return render_template('addperson.html')

@app.route('/addPerson/', methods=['POST', 'GET'])
def addPerson():
    if request.method == 'POST':
        personname = str(request.form['name'])
        persondescription = str(request.form['person_description'])
        
        if not personname:
            return render_template('addperson.html')

        elif not persondescription:
            return render_template('addperson.html')

        else:
            thisperson = People(name=personname, description=persondescription)
            db.session.add(thisperson)
            db.session.commit()
            return redirect(url_for('index'))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)