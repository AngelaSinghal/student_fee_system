import pymysql

def get_course_paid(st_id,course_id):
    con = pymysql.connect(host="localhost", port=3306, user="root", passwd="", db="student_fee", autocommit=True)
    cur = con.cursor()
    s1 = "select * from fee_transaction where st_id='"+str(st_id)+"' and course_id='"+str(course_id)+"'"
    cur.execute(s1)
    n = cur.rowcount
    t = 0
    if n > 0:
        data = cur.fetchall()
        for d in data:
            t = t + d[3]
    return t

def make_connection():
    cn = pymysql.connect(host="localhost",port=3306,db="student_fee",user="root",autocommit=True,passwd="")
    cur = cn.cursor()
    return cur
