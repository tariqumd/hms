from application import app,db
from flask import render_template,request,json,Response, redirect , flash, url_for,session
from application import User,Patient,Issued_Medicines,Medicine_MasterFile,Diagnosis,Diagnosis_MasterFile,Bed
from application.forms import Patient_Retr,Userfrom
from application import app
from flask_login import UserMixin,logout_user,current_user,login_required,login_user
from datetime import datetime
from tempfile import NamedTemporaryFile
import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator,Address
from InvoiceGenerator.pdf import SimpleInvoice

# choose english as language
os.environ["INVOICE_LANG"] = "en"



@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html",index=True)

#Login Routes
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return 'you are alraedy logged in'
    form = Userfrom()
    if form.validate_on_submit():
        user=User.query.filter_by(id=form.id.data).first()
        if user and user.password==form.password.data:
            login_user(user)
            flash('Login Sucessful','success')
            return redirect(url_for('index'))
        else:
            flash('Invalid User','danger')
            return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form, login=True)


# logout part

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


#Desk_executive


@app.route("/add_patient",methods=['POST','GET'])
@login_required
def add_patient():

    patient_ssn_id=request.form['patient_ssn_id']
    test=Patient.query.filter_by(patient_ssn_id=patient_ssn_id).first()
    if test:
        flash("Patient with this ID already exist","danger")
        return redirect('/register')
    else:
        patient_ssn_id=request.form['patient_ssn_id']
        patient_name=request.form['patient_name']
        patient_age=request.form['patient_age']
        beds=request.form['beds']
        address=request.form['address']
        state=request.form['stt']
        city=request.form['city']
        if len(patient_ssn_id) == 9:
            pat = db.session.query(Patient).order_by(Patient.patient_id.desc()).first()
            #mas_med = db.session.query(Medicine_MasterFile).get(medicine_id)
            if pat is not None:
                p_id = pat.patient_id+1
            else:
                p_id = 1

            newpatient=Patient(patient_id=p_id,patient_ssn_id=patient_ssn_id,patient_name=patient_name,patient_age=patient_age,doa=datetime.today(),beds=beds,address=address,
                                state=state,city=city,status="active")
            db.session.add(newpatient)
            db.session.commit()
            flash(f"{p_id} : Patient created successfuly","success")
            return redirect('/register')
        else:
            flash("Patient SSN id should be 9 characters ","danger")
            return redirect('/register')

@app.route("/patient_update",methods=['POST','GET'])
@login_required
def patient_update():

    patient_id=int(request.form['patient_id'])
    patient_update=Patient.query.filter_by(patient_id=patient_id).first()
    if patient_update:
        return render_template('newupdate.html',patient_update=patient_update,update=True)
    else:
        flash("Patient does not exist","danger")
        return render_template('update.html',update=True)

@app.route("/patient_update1",methods=['POST','GET'])
@login_required
def patient_update1():

    patient_ssn_id=int(request.form['patient_ssn_id'])
    patient_update=Patient.query.filter_by(patient_ssn_id=patient_ssn_id).first()

    if request.method=="POST":
        patient_update.patient_ssn_id=request.form['patient_ssn_id']
        patient_update.patient_name=request.form['patient_name']
        patient_update.patient_age=int(request.form['patient_age'])
        patient_update.beds=request.form['beds']
        #date=request.form['doa']
        #d=date+" "+"10:00:00"
        #d=list(date.split("-"))
        #year=int(d[0])
        #mon=int(d[1])
        #day=int(d[2])
        #print(d)
        #patient_update.doa=d
        patient_update.address=request.form['address']
        patient_update.state=request.form['state']
        patient_update.city=request.form['city']
        patient_update.status=request.form['status']

        db.session.commit()
        flash("Patient updated successfuly","success")
        return render_template('update.html',update=True)




@app.route("/patient_delete",methods=['POST','GET'])
@login_required
def patient_delete():

    patient_id=int(request.form['patient_id'])

    patient_delete=Patient.query.filter_by(patient_id=patient_id).first()

    if patient_delete:
        db.session.delete(patient_delete)
        db.session.commit()
        flash("Patient deleted successfuly","success")
        return render_template('newdelete.html',delete=True,patient_delete=patient_delete)
    else:
        flash("Patient does not exist","danger")
        return render_template('delete.html',delete=True)


@app.route("/register")
@login_required
def register():
    return render_template("register.html",register=True)

@app.route("/update")
@login_required
def update():
    return render_template("update.html",update=True)

@app.route("/delete")
@login_required
def delete():
    return render_template("delete.html",delete=True)

@app.route("/viewing")
@login_required
def viewing():
    if current_user.designation == "Desk_executive":
            #return render_template("pharmacy.html",pharamcy=True, patientdets=details, form=form)
            #print("this works")
        form = Patient_Retr()
        return render_template("view.html",viewing=True,form=form)
    else:
        flash("Not authorised","danger")
        return redirect('/index')


@app.route("/newview",methods=["GET","POST"])
@login_required
def newview():
    if current_user.designation == "Desk_executive":
        p_li=[]
        form = Patient_Retr()
        p_id = form.patient_id.data
        exists = Patient.query.filter_by(patient_id=p_id).scalar()
        if exists:
            patient=Patient.query.filter_by(patient_id=p_id).first()
            p_li.append(patient)
            return render_template("viewing.html",viewing=True,form=form,p_li=p_li)
        else:
            flash("Patient does not exists","danger")
            return redirect('/viewing')
    else:
        flash("Not authorised","danger")
        return redirect('/index')


@app.route("/active",methods=["GET","POST"])
@login_required
def active():
    if current_user.designation == "Desk_executive":
        patients=Patient.query.filter_by(status='active' or 'Active').all()
        return render_template('active.html',patients=patients,active=True)
    else:
        flash("Not authorised","danger")
        return redirect('/index')


#pharmacy routes

@app.route("/pharmacy",methods=['GET','POST'])
@login_required
def pharamcy():

    if current_user.designation == "pharmacist":
            #return render_template("pharmacy.html",pharamcy=True, patientdets=details, form=form)
            #print("this works")
        form = Patient_Retr()
        return render_template("pharmacy.html",pharamcy=True,form=form)
    else:
        flash("Not authorised","danger")
        return redirect('/index')


@app.route("/medicine",methods=['GET','POST'])
@login_required
def medicine():

    if current_user.designation == "pharmacist":
        form=Patient_Retr()
        #if form.validate_on_submit():
        p_li=[]
        m_li=[]
        mas_li=[]

        p_id = form.patient_id.data
        exists = Patient.query.filter_by(patient_id=p_id).scalar()
        if exists:
            details = Patient.query.filter_by(patient_id=int(p_id)).first()
            med_is = Issued_Medicines.query.filter_by(patient_id=int(p_id)).all()
            med_mas = Medicine_MasterFile.query.filter_by().all()
            p_li.append(details)
            m_li.append(med_is)
            mas_li.append(med_mas)
            #print(m_li)
                #return redirect('/index')
            return render_template("medicine.html",medicine=True, patientdets=p_li,iss_med=m_li,med_mas=mas_li,p_id=p_id, form=form)
        else:
            flash("Patient does not exists","danger")
            return redirect('/pharmacy')
    else:
        flash("Not authorised","danger")
        return redirect('/index')




@app.route("/addmed",methods=['GET','POST'])
@login_required
def addmed():
    if current_user.designation == "pharmacist":
        patient_id = request.form.get("patient_id")
        medicine_id = request.form.get("medicine_id")
        medicine_name = request.form.get("medicine_name")
        medicine_rate = request.form.get("medicine_rate")
        quantity_available = request.form.get('quantity_available')
        quantity_issued = request.form.get('qty')
        #iss_med = db.session.query(Issued_Medicines).order_by(Issued_Medicines.med_trans_id.desc()).first()
        #mas_med = db.session.query(Medicine_MasterFile).get('medicine_id')
        details = Patient.query.filter_by(patient_id=int(patient_id)).first()
        if details.status == "discharged":
            flash("Patient already discharged","danger")
            return redirect('/pharmacy')
        else:
            if int(quantity_issued) <= int(quantity_available) :
                iss_med = db.session.query(Issued_Medicines).order_by(Issued_Medicines.med_trans_id.desc()).first()
                mas_med = db.session.query(Medicine_MasterFile).get(medicine_id)
                if iss_med is not None:
                    med_trans_id = iss_med.med_trans_id+1
                else:
                    med_trans_id = 1
                mas_med.quantity_available = int(quantity_available) - int(quantity_issued)
                added = Issued_Medicines(med_trans_id=med_trans_id,patient_id=patient_id,medicine_id=medicine_id,medicine_name=medicine_name,medicine_rate=medicine_rate,quantity_issued=quantity_issued)
                db.session.add(added)
                db.session.commit()

                flash(f"{medicine_name} Issued successfuly","success")

                return redirect('/pharmacy')
            else:
                flash("Medicine not Available","danger")

                return redirect('/pharmacy')
    else:
        flash("Not authorised","danger")
        return redirect('/index')


#diagnostic Routes

@app.route("/retrieve",methods=['GET','POST'])
@login_required
def retrieve():
    if current_user.designation == "diagnostic":
        form = Patient_Retr()
        session.pop('p_id',None)
        return render_template("retrieve.html",retrieve=True,form=form)
    else:
        flash("Not authorised","danger")
        return redirect('/index')


@app.route("/tests",methods=['GET','POST'])
@login_required
def tests():
    if current_user.designation == "diagnostic":
        form=Patient_Retr()
        p_li=[]
        m_li=[]
        if request.method == 'POST':
            p_id = form.patient_id.data
            exists = Patient.query.filter_by(patient_id=p_id).scalar()
            if exists:
                session['p_id'] = int(p_id)
            else:
                flash("Patient does not exists","danger")
                return redirect('/retrieve')
        elif session['p_id'] is None:
            flash("Enter a id","danger")
            return redirect('/retrieve')
        details = Patient.query.filter_by(patient_id=session['p_id']).first()
        dia_mas = Diagnosis.query.filter_by(patient_id=session['p_id']).all()
        p_li.append(details)
        m_li.append(dia_mas)
        return render_template("tests.html",retrieve=True, patientdets=p_li,dia_mas=m_li,p_id=session['p_id'],form=form)
    else:
        flash("Not authorised","danger")
        return redirect('/index')


@app.route('/diagnostics')
@login_required
def diagnostics():
    if current_user.designation == "diagnostic":
        diagnosis = Diagnosis_MasterFile.query.all()
        return render_template("diagnostics.html", diagnosis=diagnosis, retrieve=True)
    else:
        flash("Not authorised","danger")
        return redirect('/index')

@app.route('/add',methods=['GET','POST'])
@login_required
def add():
    if current_user.designation == "diagnostic":
        p_id=request.form.get("patient_id")
        details = Patient.query.filter_by(patient_id=int(p_id)).first()
        if details.status == "discharged":
            flash("Patient already discharged","danger")
            return redirect('/retrieve')
        else:
            diagnosis_name=request.form.get("diagnosis_name")
            dia_mas = Diagnosis_MasterFile.query.filter_by(dia_name=diagnosis_name).first()
            my_data = Diagnosis(patient_id=p_id,
                                                diagnosis_name = dia_mas.dia_name,
                                                price = dia_mas.price)
            db.session.add(my_data)
            db.session.commit()
            flash(f"Diagnosis Updated successfuly","success")
            return redirect(url_for('retrieve'))
    else:
        flash("Not authorised","danger")
        return redirect('/index')


#Billing

@app.route("/billing",methods=['GET','POST'])
@login_required
def billing():
    form = Patient_Retr()
    return render_template("billing.html",billing=True,form=form)



@app.route("/bills",methods=['GET','POST'])
@login_required
def bills():
    form=Patient_Retr()
    #if form.validate_on_submit():
    p_li=[]
    m_li=[]
    d_li=[]

    p_id = form.patient_id.data
    exists = Patient.query.filter_by(patient_id=p_id).scalar()
    if exists:
        details = Patient.query.filter_by(patient_id=int(p_id)).first()
        if details.status == "discharged":
            flash("Patient already discharged","danger")
            return redirect('/index')
        else:
            med_is = Issued_Medicines.query.filter_by(patient_id=int(p_id)).all()
            dia_mas = Diagnosis.query.filter_by(patient_id=int(p_id)).all()
            p_li.append(details)
            d_li.append(dia_mas)
            m_li.append(med_is)
            mcosts = 0
            bcosts = 0
            bed =[]
            b=0
            for data in p_li:
                d = (datetime.today() - data.doa).days
                beds = Bed.query.filter_by(bed_type=data.beds).first()
                print(beds)
                bed.append(beds)
                for data in bed:
                    b = data.bed_cost
                    bcosts= d * b

            for rows in m_li:
                for data in rows:
                    mcosts += data.medicine_rate * data.quantity_issued
            dcosts = 0
            for rows in d_li:
                        for data in rows:
                            dcosts += data.price
            total = dcosts + mcosts + bcosts
            #print(m_li)
                #return redirect('/index')
            return render_template("bills.html", billing=True, patientdets=p_li, d=d,b=b,bedtot = bcosts,total = total, totdia=dcosts,totmed=mcosts,dia_mas=d_li, iss_med=m_li, p_id=p_id, form=form)
    else:
        flash("Patient does not exists","danger")
        return redirect('/billing')


#invoice generation
@app.route("/invoice",methods=['GET','POST'])
@login_required
def invoice():
    pat = request.form.get('patient')
    idn = request.form.get('id')
    name=pat+"_"+idn
    client = Client(name)
    addr = Address(add)
    provider = Provider('ABC HOSPITAL', bank_account='2600420569', bank_code='2010')
    creator = Creator('DESK EXECUTIVE')
    bed = request.form.get('bedcost')
    med = request.form.get('medcost')
    dia = request.form.get('diacost')
    tot = request.form.get('total')
    d = request.form.get('Days')

    invoice = Invoice(client, provider, creator)
    invoice.currency ='Rs'
    invoice.add_item(Item(d,bed, description="Bed cost"))
    invoice.add_item(Item(1,med, description="Medicine"))
    invoice.add_item(Item(1,dia, description="Diagnosis"))

    pdf = SimpleInvoice(invoice)
    url="application/invoice/"+pat+"_"+idn+".pdf"
    pdf.gen(url, generate_qr_code=True)

    patient_up = db.session.query(Patient).get(idn)
    patient_up.status="discharged"
    db.session.commit()
    flash("Patient Discharged , Invoice generated in Invoice folder","success")
    return redirect('/billing')
