from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from mylib import *

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def index():
    return render_template('index.html')

# login system
@app.route("/login", methods=["GET","POST"])
def login():
    if(request.method=="POST"):
        email = request.form["T1"]
        passwd = request.form["T2"]
        con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
        cur = con.cursor()
        s1 = "select * from login_data where email='"+email+"' and password='"+passwd+"'"
        cur.execute(s1)
        c = cur.rowcount
        if(c==1):
            data = cur.fetchone()
            usertype = data[2]
            #create session
            session["usertype"] = usertype
            session["email"] = email
            #open authorised pages
            if(usertype=="admin"):
                return redirect(url_for("admin_home"))
            elif(usertype=="accountant"):
                return redirect(url_for("accountant_home"))
            else:
                return render_template("login.html", msg="contact to admin")

        else:
            return render_template("login.html", msg="either email or password is incorrect")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    if 'usertype' in session:
        session.pop('usertype',None)
        session.pop('email',None)
        return redirect(url_for("login"))

    else:
        return redirect(url_for('login'))



@app.route("/admin_home")
def admin_home():
    if 'usertype' in session:
        ut = session['usertype']
        e1 = session["email"]
        if ut == 'admin':
            return render_template("admin_home.html", e1=e1)
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route("/auth_error")
def auth_error():
    return render_template("auth_error.html")

@app.route("/accountant_home")
def accountant_home():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'accountant':
            return render_template("accountnt_home.html", e1=e1)
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")

@app.route("/accountant_profile", methods=["GET","POST"])
def accountant_profile():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'accountant':
                if request.method == 'POST':
                    em = request.form['T0']
                    nm = request.form['T1']
                    des = request.form['T2']
                    contact = request.form['T3']
                    cur = make_connection()
                    s1 = "update accountant set emp_no='"+em+"', name='" + nm + "', designation='" + des + "', contact='" + contact + "' where email='" + e1 + "'"
                    cur.execute(s1)
                    a = cur.rowcount
                    if a > 0:
                        return render_template("accountant_profile.html", msg="data changes are saved")
                    else:
                        return render_template("accountant_profile.html", msg="data changes are not  saved")
                else:
                    cur = make_connection()
                    s = "select * from accountant where email='" + e1 + "'"
                    cur.execute(s)
                    a = cur.rowcount
                    if a == 1:
                        data = cur.fetchone()
                        return render_template("accountant_profile.html", data=data)
                    else:
                        return render_template("accountant_profile.html", msg="no data")

        else:
                return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))


@app.route("/st_data", methods=["GET", "POST"])
def st_data():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "GET":
                return render_template("st_data.html")
            else:
                # post
                # grab the data
                nm = request.form["T2"]
                address = request.form["T3"]
                contact = request.form["T4"]
                email = request.form["T5"]
                msg = ""
                con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
                cur = con.cursor()
                s1 = "insert into st_data values( 0, '"+nm+"', '"+address+"','"+contact+"', '"+email+"')"
                cur.execute(s1)
                n = cur.rowcount
                if n == 1:
                    msg = "Data saved"
                else:
                    msg = "No data is saved please  try again"
                return render_template("st_data.html", angela=msg)
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")

@app.route("/edit_student",methods=["GET","POST"])
def edit_student():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                st_id = request.form["H1"]
                cur = make_connection()
                s1 = "select * from st_data where st_id='"+st_id+"'"
                cur.execute(s1)
                n = cur.rowcount
                if n == 1:
                    data = cur.fetchone()
                    return render_template("edit_student.html", vgt=data)
                else:
                    return render_template("edit_student.html", msg="Error:No data found")
            else:
                return render_template("auth_error.html")
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")

@app.route("/edit_student1",methods=["GET","POST"])
def edit_student1():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                st_id = request.form["T1"]
                nm = request.form["T2"]
                address = request.form["T3"]
                contact = request.form["T4"]
                email = request.form["T5"]
                cur = make_connection()
                s1 = "UPDATE st_data SET name='"+nm+"' ,address='"+address+"' ,contact='"+contact+"' ,email='"+email+"' WHERE st_id='"+st_id+"'"
                print(s1)
                cur.execute(s1)
                n = cur.rowcount
                if n == 1:
                    msg = "data updated"
                else:
                    msg = "Error:Please try again"
                return render_template("edit_student1.html", msg=msg)
            else:
                return render_template("auth_error.html")
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")


@app.route("/show_students")
def show_students():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
            cur = con.cursor()
            s1 ="select * from st_data"
            cur.execute(s1)
            a = cur.rowcount
            if(a>0):
                data = cur.fetchall()
                return render_template("show_students.html", vgt=data)
            else:
                return render_template("show_students.html", msg="Error:please try again")
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")

@app.route("/student_course",methods=["GET","POST"])
def student_course():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                st_id = request.form["A1"]
                cur = make_connection()
                s1 = "select * from course_master"
                cur.execute(s1)
                n = cur.rowcount
                if n > 0:
                    course = cur.fetchall()
                return render_template("student_course.html", st_id=st_id, data=course)
            else:
                return render_template("student_course.html")
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")
@app.route("/student_course1", methods=["GET","POST"])
def st_course_reg1():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                st_id = request.form["T2"]
                course = request.form["T3"]
                fee = request.form["T4"]
                join_date = request.form["T5"]
                remarks = request.form["T6"]
                discount = request.form["T7"]
                cur = make_connection()
                s1 = ("insert into st_course values (0, '"+st_id+"', '"+course+"', '"+fee+"', '"+join_date+"', '"+remarks+"', '"+discount+"')")
                try:
                    cur.execute(s1)
                    n = cur.rowcount

                    if n > 0:
                        msg = "Data is saved"
                    else:
                        msg = "Data not saved"
                except pymysql.err.InternalError:
                    msg = "Data is already Registered"
                return render_template("student_course1.html", msg=msg)
            else:
                return redirect(url_for("show_students"))
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")

@app.route("/add_new_course",methods=["GET","POST"])
def new_course_reg():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                st_id = request.form["T2"]
                course = request.form["T3"]
                fee = request.form["T4"]
                join_date = request.form["T5"]
                remarks = request.form["T6"]
                discount = request.form["T7"]
                msg=""
                cur=make_connection()
                s1="insert into st_course values (0 ,'"+st_id+"' ,'"+course+"' ,'"+fee+"' ,'"+join_date+"' ,'"+remarks+"' ,'"+discount+"')"
                cur.execute(s1)
                n=cur.rowcount
                if n == 1:
                    msg="data saved"
                else:
                    msg="error:try again"
                return render_template("student_course.html",msg=msg)
            else:
                return render_template("student_course.html")
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")
@app.route("/first_fee",methods=["GET","POST"])
def first_fee():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                st_id =request.form["T1"]
                course_id = request.form["T2"]
                amount = request.form["T3"]
                deposit_date = request.form["T4"]
                remarks = request.form["T5"]
                msg=""
                cur=make_connection()
                s1="insert into fee_transaction values (0 ,'"+st_id+"' ,'"+course_id+"' ,'"+amount+"' ,'"+deposit_date+"' ,'"+remarks+"')"
                cur.execute(s1)
                n=cur.rowcount
                if n == 1:
                    msg = "data saved"
                else:
                    msg = "error:try again"
                return render_template("fee_transaction.html", msg=msg)
            else:
                return render_template("fee_transaction.html")


@app.route("/fee_transaction",methods=["GET","POST"])
def fee_transaction():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                st_id = request.form["C1"]
                return render_template("fee_transaction.html", st_id=st_id)
            else:
                return redirect(url_for("show_students"))
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")


@app.route("/fee_transaction1", methods=["GET", "POST"])
def fee_transaction_reg1():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                st_id = request.form["T1"]
                course_id = request.form["T2"]
                amount = request.form["T3"]
                deposit_date = request.form["T4"]
                remarks = request.form["T5"]
               # discount = request.form["T7"]
                cur = make_connection()
                s1 = ("insert into fee_transaction values (0, '"+st_id+"', '"+course_id+"', '"+amount+"', '"+deposit_date+"', '"+remarks+"')")
                try:
                    cur.execute(s1)
                    n = cur.rowcount

                    if n > 0:
                        msg = "Data is saved"
                    else:
                        msg = "Data not saved"
                except pymysql.err.InternalError:
                    msg = "Data is already Registered"
                return render_template("fee_transaction1.html", msg=msg)
            else:
                return redirect(url_for("show_students"))
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")

@app.route("/student_home", methods=["GET","POST"])
def student_home():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if request.method == "POST":
                st_id = request.form["H1"]
                con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
                cur = con.cursor()
                s1 = "select * from st_data where st_id='"+st_id+"'"
                cur.execute(s1)
                n = cur.rowcount
                if n > 0:
                    data = cur.fetchall()
                    s2 = "select * from st_course where st_id=" + st_id
                    cur.execute(s2)
                    m = cur.rowcount
                    if m > 0:
                        data1 = cur.fetchall()
                        # create list for student courses
                        stcourses = []
                        total_fee = 0
                        total_paid = 0
                        total_discount = 0
                        for d in data1:
                            paid = get_course_paid(d[1], d[0])
                            total_fee = total_fee+d[3]
                            total_discount = total_discount+d[6]
                            total_paid = total_paid + paid
                            due = d[3]-d[6]-paid
                            aa = [d[0], d[1], d[2], d[3], d[4], d[5], d[6], paid, due]
                            stcourses.append(aa)
                        final_total = total_fee-total_discount-total_paid
                        fee_list = [total_fee, total_discount, total_paid, final_total]
                        s3 = "select * from fee_transaction where st_id=" + st_id
                        cur.execute(s3)
                        a = cur.rowcount
                        if a > 0:
                            data2 = cur.fetchall()
                            return render_template("student_home.html", st_id=st_id, kota=data, vgt=stcourses, angela=data2, fees=fee_list)
                        else:
                            return render_template("student_home.html", st_id=st_id, kota=data, vgt=data1, fees=fee_list)
                    else:
                        return render_template("student_home.html", st_id=st_id, kota=data, msg="NO DATA FOUND")
                else:
                    return render_template("student_home.html", msg="no data found")
            else:
                return render_template("student_home.html", msg="no data found")
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")
@app.route("/admin_reg",methods=["GET","POST"])
def admin_reg():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method == "GET":
                return render_template("admin_reg.html")

            else:
                # post
                # grab the data
                a = request.form["T1"]
                b = request.form["T2"]
                c = request.form["T3"]
                d = request.form["T4"]
                e = request.form["T5"]
                f = request.form["T6"]
                usertype = "admin"
                msg=""
                if(e!=f):
                    msg= "Password not matched"
                else:
                    con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
                    cur = con.cursor()
                    s1 = "insert into admin_data values ('"+a+"', '"+b+"','"+c+"', '"+d+"')"
                    s2 = "insert into login_data values ('"+d+"', '"+e+"', '"+usertype+"')"
                    cur.execute(s1)
                    n1 = cur.rowcount
                    cur.execute(s2)
                    n2 = cur.rowcount
                    if(n1 == 1 and n2 == 1):
                        msg = "Data saved and login created"
                    elif(n1 == 1):
                        msg = "only data is saved"
                    elif(n2 == 1):
                        msg = "only login is created"
                    else:
                        msg = "error: no data is saved and no login"
                    return render_template("admin_reg.html", x=msg)

        else:
            return render_template("auth_error.html")

    else:
        return render_template("auth_error.html")

@app.route("/acc_reg",methods=["GET","POST"])
def acc_reg():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if(request.method=="GET"):
                return render_template("accountant.html")
            else:
                # post
                # grab the data
                a = request.form["T1"]
                b = request.form["T2"]
                c = request.form["T3"]
                d = request.form["T4"]
                e = request.form["T5"]
                f = request.form["T6"]
                g = request.form["T7"]
                usertype = "accountant"
                msg=""
                if(f!=g):
                    msg= "Password not matched"
                else:
                    con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
                    cur = con.cursor()
                    s1 = "insert into accountant values ('"+a+"', '"+b+"', '"+c+"', '"+d+"','"+e+"')"
                    s2 = "insert into login_data values ('"+e+"', '"+f+"', '"+usertype+"')"
                    try:
                        cur.execute(s1)
                        n1 = cur.rowcount
                        cur.execute(s2)
                        n2 = cur.rowcount
                        if(n1==1 and n2==1):
                            msg="Data saved and login created"
                        elif(n1==1):
                            msg="error:only data saved"
                        elif(n2==1):
                            msg="error:only login created"
                        else:
                            msg="error:nothing is saved"
                    except pymysql.err.IntegrityError:
                        msg="Email already registered"
                return render_template("accountant.html", x=msg)

        else:
            return render_template("auth_error.html")

    else:
        return render_template("auth_error.html")
@app.route("/show_acc")
def show_acc():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
            cur = con.cursor()
            s1 = "select * from accountant"
            cur.execute(s1)
            a = cur.rowcount
            if a > 0:
                data = cur.fetchall()
                return render_template("show_acc.html", vgt=data)
            else:
                return render_template("show_acc.html", msg="No data found")
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")
@app.route("/acc_edit")
def acc_edit():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
            cur = con.cursor()
            s1 = "select * from accountant"
            cur.execute(s1)
            a = cur.rowcount
            if (a > 0):
                data = cur.fetchall()
                return render_template("acc_edit.html", vgt=data)
            else:
                return render_template("acc_edit.html", msg="No data found")

        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")
@app.route("/edit_acc",methods=["GET","POST"])
def edit_acc():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method=="POST":
                email=request.form["h1"]
                con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
                cur = con.cursor()
                s1 = "select * from accountant where email='"+email+"'"
                cur.execute(s1)
                a = cur.rowcount
                if a==1:
                    data = cur.fetchone()
                    return render_template("edit_acc.html",vgt=data)
                else:
                    return render_template("edit_acc.html",msg="Error:no data found")
            else:
                return redirect(url_for("edit_acc"))
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")

@app.route("/edit_acc1", methods=["GET","POST"])
def edit_acc1():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if request.method=="POST":
                en = request.form["T1"]
                nm = request.form["T2"]
                des = request.form["T3"]
                conn = request.form["T4"]
                em = request.form["T5"]
                con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
                cur = con.cursor()
                s1 = "update accountant set emp_no='"+en+"', name='"+nm+"', designation='"+des+"', contact='"+conn+"' where email='"+em+"'"
                cur.execute(s1)
                a = cur.rowcount
                if a==1:
                    return render_template("edit_acc1.html", msg="Data saved successfully")
                else:
                    return render_template("edit_acc1.html",msg="Error:try again")
            else:
                return redirect(url_for("acc_edit"))
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")



@app.route("/delete_acc",methods=["GET","POST"])
def delete_acc():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if(request.method=="POST"):
                email = request.form["h1"]
                con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
                cur = con.cursor()
                s1 ="select * from accountant where email='"+email+"'"
                cur.execute(s1)
                a=cur.rowcount
                if(a==1):
                    data = cur.fetchone()
                    return render_template("delete_acc.html", vgt=data)
                else:
                    return redirect(url_for("admin_home"))
            else:
                return render_template("auth_error.html")
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")

@app.route("/delete_acc1",methods=["GET","POST"])
def delete_acc1():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'admin':
            if (request.method == "POST"):
                email = request.form["T5"]
                con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
                cur = con.cursor()
                s1 = "delete  from accountant where email='"+email+"'"
                s2 = "delete from login_data where email='"+email+"'"
                cur.execute(s1)
                a = cur.rowcount
                cur.execute(s2)
                if (a == 1):
                    return render_template("delete_acc1.html", msg="DELETION SUCCESSFUL")
                else:
                    return render_template("delete_acc1.html", msg="Error:try again")

            else:
                return redirect(url_for("show_acc"))
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")

@app.route("/add_course",methods=["GET","POST"])
def add_course():
    if 'usertype' in session:
        usertype = session['usertype']
        if usertype == 'accountant':
            if(request.method=="GET"):
                return render_template("add_course.html")
            else:
                # post
                a = request.form["T1"]
                b = request.form["T2"]
                c = request.form["T3"]
                d = request.form["T4"]
                msg=""
                con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
                cur = con.cursor()
                s1 = "insert into course_master values ('"+a+"', '"+b+"', '"+c+"', '"+d+"')"
                cur.execute(s1)
                n1 = cur.rowcount
                if(n1==1):
                    msg="course registered successfully"
                else:
                    msg="Error:course is not registered ,please try again"
                return render_template("add_course.html", x=msg)
        else:
            return render_template("auth_error.html")
    else:
        return render_template("auth_error.html")
@app.route("/show_course")
def show_course():
    con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
    cur = con.cursor()
    s1 = "select * from course_master"
    cur.execute(s1)
    a=cur.rowcount
    if(a>0):
        data = cur.fetchall()
        return render_template("show_course.html", vgt=data)
    else:
        return render_template("show_course.html", msg="No data found")

@app.route("/admin_info", methods=["GET","POST"])
def admin_info():
    if 'usertype' in session:
        usertype = session['usertype']
        e1 = session['email']
        if usertype == 'admin':
            if request.method == 'POST':
                nm = request.form['T1']
                address = request.form['T2']
                contact = request.form['T3']
                cur = make_connection()
                s1 = "update admin_data set name='"+nm+"', address='"+address+"', contact='"+contact+"' where email='"+e1+"'"
                cur.execute(s1)
                a = cur.rowcount
                if a > 0:
                    return render_template("admin_info.html", msg="data changes are saved")
                else:
                    return render_template("admin_info.html", msg="data changes are not  saved")
            else:
                cur = make_connection()
                s = "select * from admin_data where email='"+e1+"'"
                cur.execute(s)
                a = cur.rowcount
                if a == 1:
                    data = cur.fetchone()
                    return render_template("admin_info.html", data=data)
                else:
                    return render_template("admin_info.html", msg="no data")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

if (__name__=="__main__"):
    app.run(debug=True)