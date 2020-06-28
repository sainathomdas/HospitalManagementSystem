from application import app
from application import conn
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime, date
from functools import wraps
from application.models import login as login_table
from application.models import userstore as user_store_table
from application.models import patient as patient_table
from application.models import medicine as medicine_table
from application.models import medicinesIssued as medicines_issued_table
from application.models import diagnostics as diagnostics_table
from application.models import patient_diagnostics as patient_diagnostics_table


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


def is_registration_executive(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'login_type' in session and session['login_type']=='reg':
            return f(*args,*kwargs)
        else:
            session.clear()
            return redirect(url_for('login'))
    return wrap

def is_pharmacist(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'login_type' in session and session['login_type']=='pharm':
            return f(*args,*kwargs)
        else:
            session.clear()
            return redirect(url_for('login'))
    return wrap

def is_diagnostic(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'login_type' in session and session['login_type']=='diag':
            return f(*args,*kwargs)
        else:
            session.clear()
            return redirect(url_for('login'))
    return wrap
    
@app.route('/home/')
@is_logged_in
def home(login_type = None):
    return render_template('home.html', home = True)

# ------------------------------------------------------------------------------------------------------------


@app.route('/create_patient/', methods = ['GET', 'POST'])
@is_logged_in
@is_registration_executive
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
@is_registration_executive
def updatePatient():    
    return render_template('update_patient.html', activate_patient_mgmt = True)


@app.route('/get_patient/', methods = ['GET', 'POST'])
@is_logged_in
def getPatient():
    if request.method == 'POST':
        pid = request.form['pid']
        result = patient_table.read_patient(f"pid={pid}")
        if (len(result) > 0):
            session['pid'] = pid
            for row in result:
                session['pid'] = pid
                if row[9] == 'discharged':
                    session.pop('pid', None)
                    return jsonify({'error' : 'Patient has been discharged !!'})
                return jsonify(row)
                
        else:
            session.pop('pid', None)
            return jsonify({'error' : 'Patient not found !!'})

@app.route('/update_patient_into_database/', methods = ['GET', 'POST'])
@is_logged_in
@is_registration_executive
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
            flash("Patient update initiated successfully", category= 'success')
            return redirect(url_for('updatePatient'))
        else:
            flash('An unknown error occured', 'warning')
            return redirect(url_for('updatePatient'))


@app.route('/delete_patient/', methods = ['GET', 'POST'])
@is_logged_in
@is_registration_executive
def deletePatient():    
    return render_template('delete_patient.html', activate_patient_mgmt = True)


@app.route('/delete_patient_from_database/', methods = ['GET', 'POST'])
@is_logged_in
@is_registration_executive
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
@is_registration_executive
def viewPatients():
    result = patient_table.read_patient()
    return render_template('view_patient.html', datatable = True, viewPatients = True, data=result)


@app.route('/search_patient/')
@is_logged_in
@is_registration_executive
def searchPatient():
    return render_template('search_patient.html', searchPatient = True)

# =======================================================================================================


@app.route('/issue_medicines/')
@is_logged_in
@is_pharmacist
def issueMedicines():
    return render_template('issue_medicines.html', issueMedicines = True)


@app.route('/get_medicines/', methods = ['GET', 'POST'])
@is_logged_in
def getMedicines():
    if request.method == 'POST':
        pid = request.form['pid']
        result = medicines_issued_table.read_medicines_issued(f"pid={pid}")
        if (len(result) > 0):
            return jsonify(result)
        else:
            return jsonify({'error' : 'No medicines issued yet !!'})


@app.route('/add_medicines_to_database/', methods = ['GET', 'POST'])
@is_logged_in
@is_pharmacist
def addMedicinesToDatabase():
    if request.method == 'POST':
        pid = session['pid']
        for mid, medicine, qty, rate, amt in zip(request.form.getlist('mid'), request.form.getlist('medicine'), request.form.getlist('qty'), request.form.getlist('rate'), request.form.getlist('amt')):
            medicines_issued_table.insert_medicines_issued(f"{int(pid)}, {int(mid)}, '{medicine}', {int(qty)}, {float(rate)}, {float(amt)} ")            

            medicine_table_data = medicine_table.read_medicine(f"mid={mid}")
            actual_qty = 0
            for row in medicine_table_data:
                actual_qty = row[2]
            medicine_table.update_medicine(f"quantity='{int(actual_qty) - int(qty)}'", f"mid={mid}")
        
        flash('Medicines issued successfully', 'success')
        session.pop('pid', None)
        return redirect(url_for('issueMedicines'))

@app.route('/issue_new_medicines/', methods = ['GET', 'POST'])
@is_logged_in
@is_pharmacist
def issueNewMedicines():
    if 'pid' in session:
        medicines = medicine_table.read_medicine()
        return render_template('issue_new_medicines.html', issueMedicines = True, medicines = medicines)
    else:
        return redirect(url_for('issueMedicines'))


@app.route('/get_medicine_details/', methods = ['GET', 'POST'])
@is_logged_in
@is_pharmacist
def getMedicineDetails():
    if request.method == 'POST':
        mid = request.form['medicine_id'] # mid = medicine_id
        medicine_details = medicine_table.read_medicine(f"mid={mid}")
        for row in medicine_details:
            return jsonify(row)

# =======================================================================================================

@app.route('/diagnostics/', methods = ['GET', 'POST'])
@is_logged_in
@is_diagnostic
def diagnostics():
    return render_template('diagnostics.html', diagnostics = True)

@app.route('/add_diagnostics/', methods = ['GET', 'POST'])
@is_logged_in
@is_diagnostic
def addDiagnostics():
    if 'pid' in session:
        diagnostics = diagnostics_table.read_diagnostics()
        return render_template('add_diagnostics.html', diagnostics = True, diagnostic_tests = diagnostics)
    else:
        return redirect(url_for('diagnostics'))

@app.route('/get_tests_conducted/', methods = ['GET', 'POST'])
@is_logged_in
def getTestsConducted():
    if request.method == 'POST':
        pid = request.form['pid']
        result = patient_diagnostics_table.read_patient_diagnostics(int(pid))
        if (len(result) > 0):
            return jsonify(result)
        else:
            return jsonify({'error' : 'No tests conducted yet !!'})

@app.route('/get_test_details/', methods = ['GET', 'POST'])
@is_logged_in
@is_diagnostic
def getTestDetails():
    if request.method == 'POST':
        tid = request.form['test_id'] 
        test_details = diagnostics_table.read_diagnostics(f"id={tid}")
        for row in test_details:
            return jsonify(row)


@app.route('/add_tests_to_database/', methods = ['GET', 'POST'])
@is_logged_in
@is_diagnostic
def addTestsToDatabase():
    if request.method == 'POST':
        pid = session['pid']
        print(request.form.getlist('tname'))
        for tname in request.form.getlist('tname'):
            result = diagnostics_table.getTestsByName(tname)
            for row in result:
                patient_diagnostics_table.insert_patient_diagnostics(f"{int(pid)},{row[0]}")        
        flash('Diagnostics added successfully', 'success')
        session.pop('pid', None)
        return redirect(url_for('diagnostics'))


# =======================================================================================================
# Billing

@app.route('/billing/', methods = ['GET', 'POST'])
@is_logged_in
@is_registration_executive
def billing():
    return render_template('billing.html', billing = True)


# @app.route('/get_patient_for_billing/', methods = ['GET', 'POST'])
# @is_logged_in
# @is_registration_executive
# def getPatientForBilling():
#     if request.method == 'POST':
#         pid = request.form['pid']
#         result = patient_table.read_patient(f"pid={pid}")
#         if (len(result) > 0):
#             session['pid'] = pid
#             for row in result:
#                 session['pid'] = pid
#                 if row[9] == 'discharged':
#                     session.pop('pid', None)
#                     return jsonify({'error' : 'Patient has been dischared !!'})
#                 return jsonify(row)
                
#         else:
#             session.pop('pid', None)
#             return jsonify({'error' : 'Patient not found !!'})


@app.route('/discharge/', methods = ['GET', 'POST'])
@is_logged_in
@is_registration_executive
def discharge():
    if request.method == 'POST':
        pid = int(request.form['pid'])
        if patient_table.update_patient("status='discharged'", f"pid={pid}"):
            flash("Patient has been discharged!", category= 'success')
            return redirect(url_for('billing'))
        else:
            flash('An unknown error occured', 'warning')
            return redirect(url_for('billing'))
