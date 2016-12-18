from flask import Flask, jsonify, request, session, json, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
import redis

rdbb = redis.Redis(host='localhost')
rdbb.rpush("connlist", "127.0.0.1:5002")

# Database Configurations
app = Flask(__name__)
DATABASE = 'expense_mgmt'
PASSWORD = '28011989'
USER = 'root'
HOSTNAME = 'localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)
db = SQLAlchemy(app)


def CreateDB():
    def __init__(self, hostname=None):
    	if hostname != None:	
    		HOSTNAME = hostname
    import sqlalchemy
    engine = sqlalchemy.create_engine('mysql://%s:%s@%s'%(USER, PASSWORD, HOSTNAME)) # connect to server
    engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE)) #create db

#CreateDB()

class Create_Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=False)
    category = db.Column(db.String(120), unique=False)
    description = db.Column(db.String(120), unique=False)
    link = db.Column(db.String(200), unique=False)
    estimated_costs = db.Column(db.String(200), unique=False)
    submit_date = db.Column(db.String(80), unique=False)
    status = db.Column(db.String(120), unique=False)
    decision_date = db.Column(db.String(80), unique=False)
 

    def __init__(self, name, email, category, description, link, estimated_costs,
    submit_date, status, decision_date):
        self.name = name
        self.email = email
        self.category = category
        self.description = description
        self.link = link
        self.estimated_costs = estimated_costs
        self.submit_date = submit_date
        self.status = status
        self.decision_date = decision_date

#CreateDB()
#db.create_all()

@app.route('/v1/expenses/<string:id>', methods=['GET'])
def getExpense(id):
    res = Create_Expenses.query.filter_by(id=id).first_or_404()
    res_get_id = {
    'id' : res.id,
    'name' : res.name,
    'email' : res.email,
    'category' : res.category,
    'description' : res.description,
    'link' : res.link,
    'estimated_costs' : res.estimated_costs,
    'submit_date' : res.submit_date,
    'status' : "pending",
    'decision_date' : "09-10-2016"    
    }
    
    resp = jsonify(res_get_id)
    resp.status_code = 200
    return resp

@app.route('/v1/expenses', methods=['GET'])
def getExpenses():
    res_full = []
    res_full = Create_Expenses.query.all()
    results =[]
    for res in res_full:
        result_get = {
        'id' : res.id,
        'name' : res.name,
        'email' : res.email,
        'category' : res.category,
        'description' : res.description,
        'link' : res.link,
        'estimated_costs' : res.estimated_costs,
        'submit_date' : res.submit_date,
        'status' : "pending",
        'decision_date' : "09-10-2016"    
        }
        results.append(result_get)
    
    resp = jsonify(results)
    resp.status_code = 200
    return resp

    
@app.route('/v1/expenses', methods=['POST'])
def addExpense():
    CreateDB()
    db.create_all()
    request_json = request.get_json(force=True)
    expense = Create_Expenses(request.json['name'],request.json['email'],
    request.json['category'],request.json['description'],request.json['link']
    ,request.json['estimated_costs'],request.json['submit_date'],
    'pending|approved|rejected|overbudget','09-10-2016')

    db.session.add(expense)
    db.session.commit()

    id_res = db.session.query(func.max(Create_Expenses.id))
    res = Create_Expenses.query.filter_by(id=id_res).first()
    result_query = {
    'id' : res.id,
    'name' : res.name,
    'email' : res.email,
    'category' : res.category,
    'description' : res.description,
    'link' : res.link,
    'estimated_costs' : res.estimated_costs,
    'submit_date' : res.submit_date,
    'status' : "pending",
    'decision_date' : "09-10-2016"    
    }

    resp = jsonify(result_query)
    resp.status_code = 201
    return resp

@app.route('/v1/expenses/<string:id>', methods=['PUT'])
def updateExpense(id):
    
    request_json=request.get_json(force=True)
    res = Create_Expenses.query.filter_by(id=id).first_or_404()
    res.estimated_costs = request_json['estimated_costs']
    
    db.session.commit()
    
    update_query= {
    'estimated_costs' : res.estimated_costs   
    }

    resp = jsonify(update_query)
    resp.status_code = 202
    return resp

@app.route('/v1/expenses/<string:id>', methods=['DELETE'])
def deleteExpense(id):
    
    res = Create_Expenses.query.filter_by(id=id).first()
    db.session.delete(res)
    db.session.commit()
    resp = Response(status=204, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(debug=False,host='localhost', port='5002')
