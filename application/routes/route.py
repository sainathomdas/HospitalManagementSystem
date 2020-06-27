from application import app
from application import conn
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime, date
from functools import wraps
from application.models import login as login_table
from application.models import userstore as user_store_table
from application.models import patient as patient_table


@app.route('/')
@app.route('/login',methods = ['GET', 'POST'])
def login():
    if 'logged_in' in session:
        if session['logged_in']:
            return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_type = request.form['login_type']
        result = login_table.read_logins(f"username='{username}' and role='{login_type}'")
        if(len(result)>0):
            for row in result:
                if(username == row[0] and password == row[1]):
                    session['logged_in'] = True
                    session['username'] = username
                    session['login_type'] = login_type
                    user_store_table.insert_user_store(f"'{username}','{str(datetime.now().strftime('%Y/%m/%d, %H:%M:%S'))}'")
                
                    # flash("Successfully Logged In","success")
                    return render_template('home.html', home = True)
                else:
                    flash("Wrong password!! Try Again !!",category= "warning")
                    return redirect(url_for('login'))
        else:
            flash("Invalid Username","warning")
            return redirect(url_for('login'))
    return render_template('login.html', login_page = True)


# Declaring a decorator to check if user is logged in (Authorization)
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,*kwargs)
        else:
            flash('Must be logged in to process','warning')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout/')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out !','success')
    return redirect(url_for('login'))
    
@app.route('/home/')
@is_logged_in
def home(login_type = None):
    return render_template('home.html', home = True)

# ------------------------------------------------------------------------------------------------------------


@app.route('/create_patient/', methods = ['GET', 'POST'])
@is_logged_in
def createPatient():
    if request.method == 'POST':
        ssnid = int(request.form['ssnid'])
        pname = request.form['pname']
        page = request.form['page'] #page = patient_age
        paddress = request.form['paddress']
        doa = request.form['doa'] #doa = date of admission
        type_of_bed = request.form['type_of_bed']
        pstate = request.form['pstate']
        pcity = request.form['pcity']
        result = patient_table.read_patient(f"ssnid={ssnid} and status='Active'")
        if(len(result)>0):
            flash(f"Patient with ssnid = {ssnid} already exists!",category="warning")
            return redirect(url_for('createPatient'))

        result = patient_table.getLastRow()
        prev_pid = None
        for row in result:
            prev_pid = row[0]
        
        if prev_pid != None:        
            pid = int(prev_pid) + 1
        else:
            pid = 100000001

        if patient_table.insert_patient(f"{int(pid)}, {int(ssnid)}, '{pname}',{page}, '{doa}', '{type_of_bed}', '{paddress}','{pcity}','{pstate}','Active'"):
            flash('Patient creation initiated successfully', 'success')
            return render_template('create_patient.html', activate_patient_mgmt = True)
        else:
            flash('An unknown error occured', 'warning')
            return render_template('create_patient.html', activate_patient_mgmt = True)
    return render_template('create_patient.html', activate_patient_mgmt = True)


@app.route('/update_patient/', methods = ['GET', 'POST'])
@is_logged_in
def updatePatient():    
    return render_template('update_patient.html', activate_patient_mgmt = True)


@app.route('/get_patient/', methods = ['GET', 'POST'])
@is_logged_in
def getPatient():
    if request.method == 'POST':
        pid = request.form['pid']
        result = patient_table.read_patient(f"pid={pid}")
        print(len(result))
        if (len(result) > 0):
            for row in result:
                print(row)
                return jsonify(row)
        else:
            return jsonify({'error' : 'Patient not found !!'})

@app.route('/update_patient_into_database/', methods = ['GET', 'POST'])
@is_logged_in
def updatePatientIntoDatabase():
    if request.method == 'POST':
        pid = int(request.form['pid'])
        pname = request.form['pname']
        page = int(float(request.form['page']))
        doa = request.form['doa']
        type_of_bed = request.form['type_of_bed']
        paddress = request.form['paddress']
        pstate = request.form['pstate']
        pcity = request.form['pcity']
        if patient_table.update_patient(f"name='{pname}', age={page},dateOfAdmission='{doa}',typeOfBed='{type_of_bed}' ,address='{paddress}', city='{pcity}', state = '{pstate}'", f"pid={pid}"):
            flash("Updated Successfully", category= 'success')
            return redirect(url_for('updatePatient'))
        else:
            flash('An unknown error occured', 'warning')
            return redirect(url_for('updatePatient'))


@app.route('/delete_patient/', methods = ['GET', 'POST'])
@is_logged_in
def deletePatient():    
    return render_template('delete_patient.html', activate_patient_mgmt = True)


@app.route('/delete_patient_from_database/', methods = ['GET', 'POST'])
@is_logged_in
def deletePatientFromDatabase():    
    if request.method == 'POST':
        pid = int(request.form['pid'])
        if patient_table.delete_patient(f"pid={pid}"):
            flash("Successfully Deleted !!","success")
        else:
            flash('An unknown error occured', 'warning')
        return redirect(url_for('deletePatient'))


@app.route('/view_patients/')
@is_logged_in
def viewPatients():
    result = patient_table.read_patient()
    return render_template('view_patient.html', datatable = True, viewPatients = True, data=result)


@app.route('/search_patient/')
@is_logged_in
def searchPatient():
    return render_template('search_patient.html', searchPatient = True)