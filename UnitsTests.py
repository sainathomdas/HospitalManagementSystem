'''
PLEASE TURN OFF LOGIN AUTHENTICATION FOR TESTING
'''
import os
import unittest
import sqlite3

from application import app


TEST_DB = 'DATABASE.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        # db.drop_all()
        # db.create_all()

        # Disable sending emails during unit testing
        # mail.init_app(app)
        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ########################
    #### helper methods ####
    ########################

    ## helper methods for login test ##
    def login(self, email, password, login_type):
        return self.app.post('/login', data=dict(username=email, password=password, login_type=login_type), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    ## helper methods for patient management test ##
    def createpatient(self, ssnid, pname, page, doa, paddress, type_of_bed, pstate, pcity):
        return self.app.post('/create_patient/', data=dict(ssnid=ssnid, pname=pname, page=int(page), doa=doa, paddress=paddress, type_of_bed=type_of_bed, pstate=pstate, pcity=pcity), follow_redirects=True)

    def updatepatient(self, pid, pname, page, doa, type_of_bed, paddress, pstate, pcity):
        return self.app.post('/update_patient_into_database/', data=dict(pid=pid, pname=pname, page=page, doa=doa, type_of_bed=type_of_bed, paddress=paddress, pstate=pstate, pcity=pcity), follow_redirects=True)

    def deletepatient(self, pid):
        return self.app.post('/delete_patient_from_database/', data=dict(pid=pid), follow_redirects=True)

    ## helper methods for issuing medicines test ##

    def getmedicines(self, pid):
        return self.app.post('/get_medicines/', data=dict(pid=pid), follow_redirects=True)

    def gettestsconducted(self, pid):
        return self.app.post('/get_tests_conducted/', data=dict(pid=pid), follow_redirects=True)

    def gettestdetails(self, test_id):
        return self.app.post('/get_test_details/', data=dict(test_id=test_id), follow_redirects=True)

    def discharge(self, pid):
        return self.app.post('/discharge/', data=dict(pid=pid), follow_redirects=True)
    ###############
    #### tests ####
    ###############


class LoginTests(BasicTests):

    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ABC Hospital | Login', response.data)

    def test_valid_user_login(self):
        response = self.login('admin', 'admin', 'reg')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ABC Hospital | Home', response.data)

    def test_invalid_user_login(self):
        response = self.login('admin'+'x', 'admin', 'reg')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ABC Hospital | Login', response.data)

    def test_invalid_password_login(self):
        response = self.login('admin', 'admin'+'x', 'reg')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ABC Hospital | Login', response.data)


class PatientManagementTest(BasicTests):

    def test_create_patient(self):
        response = self.createpatient(100000057, 'Joe', 30, '2020-06-26',
                                      'Parklane secunderabad', 'semi_sharing', 'telangana', 'hyderabad')
        print(response)
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'create_patient',response.data)

    def test_create_patient_wrong(self):
        response = self.createpatient(
            100000023, 'Joe', 30, 'Parklane secunderabad', '2020-76-26', 'semi_sharing', 'telangana', 'hyderabad')
        print(response)
        self.assertEqual(response.status_code, 200)
        # self.assertIn(b'create_patient',response.data)

    # updatepatient(self,pid,pname,page,doa,type_of_bed,paddress,pstate,pcity)
    def test_update_patient(self):
        response = self.updatepatient(
            100000001, 'malik', 99, '2013-11-11', 'semi_sharing', 'as rao nagar', 'ap', 'hyd')
        self.assertEqual(response.status_code, 200)

    def test_delete_patient(self):
        response = self.deletepatient(100000002)
        self.assertEqual(response.status_code, 200)


class IssueMedicinesTest(BasicTests):
    def test_get_medicines_wrong(self):
        response = self.getmedicines(100000001)
        self.assertIn(b'No medicines issued yet !!', response.data)

    def test_get_medicines(self):
        response = self.getmedicines(100000007)
        # self.assertIn(b'paracetomol',response.data)
        self.assertEqual(response.status_code, 200)


class DiagnosticsTest(BasicTests):
    def test_diagnostics_page(self):
        response = self.app.get('/diagnostics/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_get_tests_conducted(self):
        response = self.gettestsconducted(100000007)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No tests conducted yet !!', response.data)


class BillingTest(BasicTests):
    def test_billing_page(self):
        response = self.app.get('/billing/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_discharge_page(self):
        response = self.discharge(100000007)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
    '''PLEASE TURN OFF LOGIN AUTHENTICATION FOR TESTING'''
