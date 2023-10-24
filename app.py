from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, insert, update, delete, and_, or_, not_, desc, asc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1100), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.id

#go to main page
@app.route('/')
def index():
    people = db.session.execute(select(People)).scalars().all()
    return render_template('index.html', people=people, totpeople = people)

#go to admin page
@app.route('/admin')
def admin():
    return render_template('admin.html')

#remove person functionality
@app.route('/removePerson/', methods=['POST', 'GET'])
def removePerson():
    if request.method == 'POST':
        personname = str(request.form['personname'])
        db.session.execute(delete(People).where(People.name.ilike(personname)))
        db.session.commit()
        return render_template('admin.html')
    else:
        return redirect(url_for('index'))

#go to add person page
@app.route('/addPerson', methods=['GET', 'POST'])
def addPersonBtn():
    return render_template('addperson.html')

#add person functionality
@app.route('/addPersonFunc', methods=['POST', 'GET'])
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
        
#search for people
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        if request.form['search'] == '':
            return redirect(url_for('index'))
        else:
            totalpeople = db.session.execute(select(People)).scalars().all()
            searchname = request.form['search']
            searchresult = db.session.execute(select(People).filter(People.name.ilike(searchname))).scalars().all()
            return render_template('index.html', people = searchresult, totpeople = totalpeople)


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=4000)