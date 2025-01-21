from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
# from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import re
from flask_wtf import CSRFProtect 
from flask_session import Session
import logging
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

load_dotenv() 
app = Flask(__name__)

app.secret_key = os.getenv('app.secret_key')
db_pw_secret = os.getenv('db_pw_secret')

csrf = CSRFProtect(app) 

bcrypt = Bcrypt(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

logging.basicConfig (
   filename = "LibMgtSys.log",
   level = logging.WARNING,                
   format = "[%(asctime)s] - %(levelname)s in %(module)s: %(message)s" 
)

try:
   db_connect = mysql.connector.connect(
      host= os.getenv('db_host'),
      user= os.getenv('db_user'),
      password= os.getenv('db_password'),
      database= os.getenv('db_database')   
   )
   app.logger.info ("DB CONNECTED...")   
   
except mysql.connector.Error as e:
   app.logger.warning ("DB NOT CONNECTED...")   


# try:
#     db_connect = mysql.connector.connect(
#        host= os.getenv('paw_db_host'),
#        user= os.getenv('paw_db_user'),
#        password= os.getenv('paw_db_password'),
#        database= os.getenv('paw_db_database')
#     )
#     app.logger.info ("DB CONNECTED...")
# except mysql.connector.Error as e:
#     app.logger.warning ("DB NOT CONNECTED...")



@app.route('/home/', methods=["GET"])
def home():
   if not session.get("username"):
        return redirect("/login/")   
   return render_template("index.html")


@app.route('/', methods=["GET"])
@app.route('/login/', methods =['GET', 'POST'])
def login():
   msg = ''
   if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
      username = request.form['username']
      password = request.form['password']   
      cursor = db_connect.cursor()      
      cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
      account = cursor.fetchone()     
      
      if cursor.rowcount == 0:        
         msg = "User ID not found...Please register if you don't have an User ID !!!"        
      else:    
         stored_password = account[2]
         if bcrypt.check_password_hash(stored_password, password):            
            session['loggedin'] = True
            # session['id'] = account['user_id']
            session['username'] = username            
            return render_template('index.html')
         else:
            msg = 'Incorrect username / password !'    

      cursor.close()              
      
   return render_template('login.html', msg = msg)


@app.route('/logout/')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('logout.html')

@app.route('/register/', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']        
        cursor = db_connect.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            hashed_password =  bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, hashed_password, email, ))
            db_connect.commit()
            cursor.close()
            msg = 'You have successfully registered !'
            return render_template('login.html', msg = msg)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'

    return render_template('register.html', msg = msg)


@app.route("/admin/", methods=["GET", "POST"])
def admin():
   if not session.get("username"):
      return redirect("/login/")  
   return render_template("admin.html")


@app.route("/student/", methods=["GET", "POST"])
def student():
   if not session.get("username"):
      return redirect("/login/") 
   
   if request.method == "POST":
      std_id = request.form["studentId"]
      std_name = request.form["studentName"]
      std_grade = request.form["studentGrade"]
      std_section = request.form["studentSection"]

      cursor = db_connect.cursor()
      sql_query = "insert into students (student_id, student_name, student_grade, student_section) values (%s,%s,%s,%s);"
      cursor.execute (sql_query, (std_id,std_name,std_grade,std_section))
      db_connect.commit()
      cursor.close()
      flash("Student Data has been added !!!")
      return render_template("admin.html"),200
   else:
      return render_template("admin.html"),200

@app.route("/student/<int:student_id>/", methods=["GET"])
def student_id(student_id):
   if not session.get("username"):
      return redirect("/login/") 
   
   cursor = db_connect.cursor(dictionary=True)
   cursor.execute("select * from students where student_id = %s;",(student_id,))

   std_record=cursor.fetchall()
   cursor.close()
   flash ("Student record with student_ID {student_id} has been fetched !!!")
   return std_record

@app.route("/librarian/")
def librarian():
   if not session.get("username"):
      return redirect("/login/")    
   return render_template("librarian.html"),200

@app.route("/reports/", methods=["GET", "POST"])
def reports():
   if not session.get("username"):
      return redirect("/login/") 
   return render_template("reports.html",data=0,data1=0,data2=0),200

@app.route("/reports/student", methods=["GET", "POST"])
def reports_student():
   if not session.get("username"):
      return redirect("/login/") 

   if request.method == "POST":
      id = int(request.form["studentId"])
      cursor = db_connect.cursor()
      sql_query = "select * from students where student_id = %s;"
      cursor.execute (sql_query, (id,))
      std_record=cursor.fetchone()
      if cursor.rowcount == 0:
         flash("There is no record available for this id !!!")

      # getting the bood details for the student_id as well 
      sql_query1 = "select book_id from books where allocated_to_id = %s;"
      cursor.execute (sql_query1, (id,))
      std_record1=cursor.fetchall()
            
      if cursor.rowcount == 0:
         books = "None"
      else:
         books = ""
         for row in std_record1:
            books += (str(row[0]) + ",  ")            

      cursor.close()
      return render_template("reports.html", data=std_record,data1=0,data2=0,data3=books,data4=""),200
   else:
      return render_template("reports.html",data=0,data1=0,data2=0,data3="",data4=""),200


@app.route("/reports/teacher", methods=["GET", "POST"])
def reports_teacher():
   if not session.get("username"):
      return redirect("/login/") 
   if request.method == "POST":
      id = int(request.form["teacherId"])
      cursor = db_connect.cursor()
      sql_query = "select * from teachers where teacher_id = %s;"
      cursor.execute (sql_query, (id,))
      std_record=cursor.fetchone()
      if cursor.rowcount == 0:
         flash("There is no record available for this id !!!")

      # getting the bood details for the student_id as well 
      sql_query1 = "select book_id from books where allocated_to_id = %s;"
      cursor.execute (sql_query1, (id,))
      std_record1=cursor.fetchall()
          
      if cursor.rowcount == 0:
         books = "None"
      else:
         books = ""
         for row in std_record1:
            books += (str(row[0]) + ",  ") 

      cursor.close()
      return render_template("reports.html", data=0,data1=std_record,data2=0,data3="",data4=books),200
   else:
      return render_template("reports.html", data=0,dataq=0,data2=0,data3="",data4=""),200

@app.route("/reports/book", methods=["GET", "POST"])
def reports_book():
   if not session.get("username"):
      return redirect("/login/") 
   
   if request.method == "POST":
      id = int(request.form["bookId"])
      cursor = db_connect.cursor()
      sql_query = "select * from books where book_id = %s;"
      cursor.execute (sql_query, (id,))
      std_record=cursor.fetchone()
      cursor.close()
      if cursor.rowcount == 0:
         flash("There is no record available for this id !!!")

      return render_template("reports.html", data=0,data1=0,data2=std_record,data3="",data4=""),200
   else:
      return render_template("reports.html",data=0,data1=0,data2=0,data3="",data4=""),200


@app.route("/student/update", methods=["GET", "POST"])
def std_edit():
   if not session.get("username"):
      return redirect("/login/") 
   
   if request.method == "POST":
      std_id = request.form["studentId"]
      std_name = request.form["studentName"]
      std_grade = request.form["studentGrade"]
      std_section = request.form["studentSection"]

      cursor = db_connect.cursor()
      sql_query = "update students set student_name=%s, student_grade=%s, student_section=%s where student_id=%s;"
      cursor.execute (sql_query, (std_name,std_grade,std_section,std_id,))
      db_connect.commit()
      cursor.close()
      flash("Student Data has been updated !!!")
      return render_template("admin.html"),200
   else:
      return render_template("admin.html"),200

@app.route("/student/delete", methods=["GET", "POST"])
def std_delete():
   if not session.get("username"):
      return redirect("/login/") 

   if request.method == "POST":
      std_id = request.form["studentId"]

      cursor = db_connect.cursor()
      sql_query = "delete from students where student_id=%s;"
      cursor.execute (sql_query, (std_id,))
      db_connect.commit()
      cursor.close()
      flash("Student Data has been deleted !!!")
      return render_template("admin.html"),200
   else:
      return render_template("admin.html"),200


@app.route("/student/get", methods=["GET", "POST"])
def std_get():
   if not session.get("username"):
      return redirect("/login/") 
   
   if request.method == "POST":
      id = int(request.form["studentId"])
      cursor = db_connect.cursor()
      sql_query = "select * from students where student_id = %s;"
      cursor.execute (sql_query, (id,))
      std_record=cursor.fetchone()
      cursor.close()
      
      return render_template("admin.html", data=std_record),200
   else:
      return render_template("admin.html",data=0),200


@app.route("/teacher_add/", methods=["GET", "POST"])
def teacher_add():
   if not session.get("username"):
      return redirect("/login/") 
   
   if request.method == "POST":
      teacher_id = request.form["teacherId"]
      teacher_name = request.form["teacherName"]
      teacher_email = request.form["teacherEmail"]

      cursor = db_connect.cursor()
      sql_query = "insert into teachers (teacher_id, teacher_name, teacher_email) values (%s,%s,%s);"
      cursor.execute (sql_query, (teacher_id,teacher_name,teacher_email,))
      db_connect.commit()
      cursor.close()
      flash("Teacher Data has been added !!!")
      return render_template("admin.html"),200
   else:
      return render_template("admin.html"),200


@app.route("/teacher_delete/", methods=["GET", "POST"])
def teacher_delete():
   if not session.get("username"):
      return redirect("/login/") 

   if request.method == "POST":
      teacher_id = request.form["teacherId"]

      cursor = db_connect.cursor()
      sql_query = "delete from teachers where teacher_id=%s;"
      cursor.execute (sql_query, (teacher_id,))
      db_connect.commit()
      cursor.close()
      flash("Teacher Data has been deleted !!!")
      return render_template("admin.html"),200
   else:
      return render_template("admin.html"),200

@app.route("/teacher/update", methods=["GET", "POST"])
def teacher_edit():
   if not session.get("username"):
      return redirect("/login/") 
      
   if request.method == "POST":
      teacher_id = request.form["teacherId"]
      teacher_name = request.form["teacherName"]
      teacher_email = request.form["teacherEmail"]

      cursor = db_connect.cursor()
      sql_query = "update teachers set teacher_name=%s, teacher_email=%s where teacher_id=%s;"
      cursor.execute (sql_query, (teacher_name,teacher_email,teacher_id,))
      db_connect.commit()
      cursor.close()
      flash("Teacher Data has been updated !!!")
      return render_template("admin.html"),200
   else:
      return render_template("admin.html"),200



@app.route("/book_add/", methods=["GET", "POST"])
def book_add():
   if not session.get("username"):
      return redirect("/login/") 

   if request.method == "POST":
      book_id = request.form["bookId"]
      book_title = request.form["bookTitle"]
      book_author = request.form["bookAuthor"]
      book_subject = request.form["bookSubject"]
      book_availability = request.form["bookAvailability"]
      book_allocatedId = request.form["bookAllocatedId"]
      issue_date = request.form["bookIssueDate"]
      return_date = request.form["bookReturnDate"]

      cursor = db_connect.cursor()
      # sql_query = "insert into books (book_id,book_title,book_author,book_subject,book_availability,allocated_to_id,issue_date,return_date) values (%s,%s,%s,%s,%s,%s,%s,%s);"
      # cursor.execute (sql_query, (book_id,book_title,book_author,book_subject,book_availability,book_allocatedId,issue_date,return_date,))
      sql_query = "insert into books (book_id,book_title,book_author,book_subject,book_availability) values (%s,%s,%s,%s,%s);"
      cursor.execute (sql_query, (book_id,book_title,book_author,book_subject,"Yes",))

      db_connect.commit()
      cursor.close()
      flash("Book Data has been added !!!")
      return render_template("admin.html"),200
   else:
      return render_template("admin.html"),200


@app.route("/book_delete/", methods=["GET", "POST"])
def book_delete():
   if not session.get("username"):
      return redirect("/login/") 

   if request.method == "POST":
      book_id = request.form["bookId"]

      cursor = db_connect.cursor()
      sql_query = "delete from books where book_id=%s;"
      cursor.execute (sql_query, (book_id,))
      db_connect.commit()
      cursor.close()
      flash("Book Data has been deleted !!!")
      return render_template("admin.html"),200
   else:
      return render_template("admin.html"),200

@app.route("/book/update", methods=["GET", "POST"])
def book_edit():
   if not session.get("username"):
      return redirect("/login/") 

   if request.method == "POST":
      book_id = request.form["bookId"]
      book_title = request.form["bookTitle"]
      book_author = request.form["bookAuthor"]
      book_subject = request.form["bookSubject"]
      book_availability = request.form["bookAvailability"]
      book_allocatedId = request.form["bookAllocatedId"]
      issue_date = request.form["bookIssueDate"]
      return_date = request.form["bookReturnDate"]

      cursor = db_connect.cursor()
      sql_query = "update books set book_title=%s,book_author=%s,book_subject=%s,book_availability=%s,allocated_to_id=%s,issue_date=%s,return_date=%s where book_id=%s;"
      cursor.execute (sql_query, (book_title,book_author,book_subject,book_availability,book_allocatedId,issue_date,return_date,book_id,))
      db_connect.commit()
      cursor.close()
      flash("Book Data has been updated !!!")
      return render_template("admin.html"),200
   else:
      return render_template("admin.html"),200


@app.route("/book/issue", methods=["GET", "POST"])
def book_issue():
   if not session.get("username"):
      return redirect("/login/") 

   if request.method == "POST":
      member_id = request.form["memberId"]
      book_id = request.form["bookId"]
      date = request.form["issueDate"]

      cursor = db_connect.cursor()
      sql_query = "update books set book_availability='No', allocated_to_id=%s, issue_date=%s, return_date=null  where book_id=%s;"
      cursor.execute (sql_query, (member_id, date, book_id,))
      db_connect.commit()
      cursor.close()
      flash("Book has been issued !!!")
      return render_template("librarian.html"),200
   else:
      return render_template("librarian.html"),200


@app.route("/book/return", methods=["GET", "POST"])
def book_return():
   if not session.get("username"):
      return redirect("/login/") 

   if request.method == "POST":
      member_id = request.form["memberId"]
      book_id = request.form["bookId"]
      date = request.form["returnDate"]
      
      cursor = db_connect.cursor()
      sql_query = "update books set book_availability='Yes', issue_date=null, allocated_to_id=0, return_date=%s  where book_id=%s;"
      cursor.execute (sql_query, (date, book_id,))
      db_connect.commit()
      cursor.close()
      flash("Book Return Data has been updated !!!")
      return render_template("librarian.html"),200
   else:
      return render_template("librarian.html"),200


if __name__ == "__main__":
   app.run(debug=True)


