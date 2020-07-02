from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_login import LoginManager
from flask_login import UserMixin,logout_user,current_user,login_required,login_user
from datetime import date,datetime
import os
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db=SQLAlchemy(app)
login_manager=LoginManager(app)
login_manager.init_app(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('database created!')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

'''
    db.session.add_all([
                User(id="911",password="abchospital",time=datetime.today(),designation="Desk_executive"),
                User(id="912",password="abchospital",time=datetime.today(),designation="pharmacist"),
                User(id="913",password="abchospital",time=datetime.today(),designation="diagnostic"),
                Medicine_MasterFile(medicine_id = "1",quantity_available = "50",medicine_name = "corgard",Rate_ofMedicine = "500"),
                Medicine_MasterFile(medicine_id = "2",quantity_available = "100",medicine_name = "tenormin",Rate_ofMedicine = "100"),
                Patient(ssn_id="5001",patient_id="101",patient_name="Jai",age="14",bed_type="general",address="Anna nagar", city="chennai", state="tn",status="active"),
                Patient(ssn_id="5002",patient_id="102",patient_name="Akhil",age="19",bed_type="single",address="Triplicane", city="chennai", state="tn",status="active"),



    ])'''

@app.cli.command('db_seed')
def db_seed():
    db.session.add_all([

                User(id="12345671",password="abc@hospital",time=datetime.today(),designation="Desk_executive"),
                User(id="12345672",password="abc@hospital",time=datetime.today(),designation="pharmacist"),
                User(id="12345673",password="abc@hospital",time=datetime.today(),designation="diagnostic"),
                Medicine_MasterFile(medicine_id = "1",quantity_available = "50",medicine_name = "corgard",Rate_ofMedicine = "500"),
                Medicine_MasterFile(medicine_id = "2",quantity_available = "100",medicine_name = "tenormin",Rate_ofMedicine = "100"),
                Medicine_MasterFile(medicine_id = "3",quantity_available = "200",medicine_name = "Dolo650",Rate_ofMedicine = "5"),
                Medicine_MasterFile(medicine_id = "4",quantity_available = "500",medicine_name = "Vitamin E",Rate_ofMedicine = "10"),
                Medicine_MasterFile(medicine_id = "5",quantity_available = "100",medicine_name = "Crocin",Rate_ofMedicine = "50"),
                Patient(patient_ssn_id="9965163534",patient_id="1",patient_name="Akhil",patient_age="19",doa=date(2020,6,20),beds="single",address="Triplicane", city="chennai", state="tn",status="active"),
                Diagnosis(patient_id="101",diagnosis_name = "ECG",price = "4000"),
                Diagnosis_MasterFile(dia_name = "ECG",price = "4000"),
                Diagnosis_MasterFile(dia_name = "MRI",price = "2500"),
                Diagnosis_MasterFile(dia_name = "CTSCAN",price = "2000"),
                Diagnosis_MasterFile(dia_name = "XRAY",price = "500"),
                Diagnosis_MasterFile(dia_name = "ULTRASOUND",price = "1500"),
                Diagnosis_MasterFile(dia_name = "BLOOD TEST",price = "1000"),
                Diagnosis_MasterFile(dia_name = "ENDOSCOPY",price = "1700"),

                Bed(bed_type="general ward",bed_cost = "2000"),
                Bed(bed_type="semi sharing",bed_cost = "4000"),
                Bed(bed_type="single room",bed_cost = "8000"),


            ])
    db.session.commit()
    print('db_seeded')




#database class
class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    time= db.Column(db.DateTime,nullable=False,default=datetime.utcnow())
    designation= db.Column(db.String(20),nullable=False)


    def __repr__(self):
        return f"User('{self.id}','{self.password}','{self.time}','{self.designation}')"

class Patient(db.Model):
    __tablename__='Patients'

    patient_id=db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    patient_ssn_id=db.Column(db.Integer,unique=True)
    patient_name=db.Column(db.String)
    patient_age=db.Column(db.Integer)
    doa=db.Column(db.DateTime)
    beds=db.Column(db.String)
    address=db.Column(db.String)
    state=db.Column(db.String)
    city=db.Column(db.String)
    status=db.Column(db.String)


class Issued_Medicines(db.Model):
    __tablename__ = 'Issued_Medicines'
    med_trans_id = Column(Integer,primary_key=True)
    patient_id = Column(Integer)
    medicine_id = Column(Integer)
    medicine_name = Column(String)
    quantity_issued = Column(Integer)
    medicine_rate = Column(Integer)

class Medicine_MasterFile(db.Model):
    __tablename__ = 'Medicine_MasterFile'
    medicine_id = Column(Integer, primary_key=True)
    medicine_name = Column(String)
    quantity_available = Column(Integer)
    Rate_ofMedicine = Column(Integer)

class Diagnosis_MasterFile(db.Model):
    __tablename__ = 'Diagnosis_MasterFile'
    dia_name = Column(String,primary_key=True)
    price = Column(Integer)
    def __init__(self,dia_name,price):
        self.dia_name = dia_name
        self.price = price

    def __repr__(self):
        return "<DIAGNOSIS{}}>".format(self.Diagnosis_MasterFile)

class Diagnosis(db.Model):
    __tablename__ = 'Diagnosis'
    diagnosis_id = Column(Integer,primary_key=True)
    patient_id = Column(Integer)
    diagnosis_name = Column(String)
    price = Column(Integer)
    def __repr__(self):
        return "<Diagnosis{}}>".format(self.Diagnosis)


class Bed(db.Model):
    __tablename__ = 'Bed'
    bed_type = db.Column(db.String,primary_key=True,nullable=False)
    bed_cost = db.Column(db.Integer,nullable=False)
    #def __repr__(self):
    #    return "<Bed{}}>".format(self.Bed)




from application import routes
from application import models
if __name__=="__main__":
    app.run(debug=True)
