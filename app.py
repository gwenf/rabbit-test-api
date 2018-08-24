import os
import json
import itertools
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/cats'
db = SQLAlchemy(app)

class Cat(db.Model):
    __tablename__ = "cats"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name 

    def __repr__(self):
        return "<Name %r>" % self.name

@app.route("/")
def index():
    return "Welcome to Cat Haven."

@app.route("/cats", methods=["GET", "POST"])
def cats():
    name = "default"

    if request.method == "POST":
        data = request.form.get("name")
        if not db.session.query(Cat).filter(Cat.name == name).count():
            reg = Cat(name)
            db.session.add(reg)
            db.session.commit()
            print(data)
            return "Success"
        return "Cat has already been added."

    if request.method == 'GET':
        temp = db.session.query(Cat).all()
        print(temp)
        d = dict(itertools.zip_longest(*[iter(temp)] * 2, fillvalue="")) 
        return d

    return "Not a valid method."

@app.route("/cats/<cat_id>")
def get_cat(cat_id):
    return cat_id

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

