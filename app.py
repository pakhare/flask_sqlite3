from flask import Flask
from flask import render_template, request
import sqlite3

app = app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html");
    
@app.route("/student/create")  
def add_student():  
    return render_template("addStudent.html")  
    
@app.route("/student/add", methods = ["POST","GET"])  
def addStudent():  
 
	if request.method == "POST":  
	    try:
	    	student_name = request.form["name"]
	    	student_email = request.form["email"]
	    	with sqlite3.connect("student.db") as conn:
		    	curr = conn.cursor()
		    	curr.execute("INSERT into students (name, email) values (?, ?)",(student_name, student_email))
	    	conn.commit()
	    	res = "Added New Student Successfully"
	    except:
	    	conn.rollback()
	    	res = "Problem while adding a student. Student not added."
	    finally:
	    	return render_template("add_msg.html", status = res)
	    	conn.close()
	    
	    
@app.route('/student/list')
def list_students():
   conn = sqlite3.connect("student.db")
   conn.row_factory = sqlite3.Row
   
   curr = conn.cursor()
   curr.execute("SELECT * FROM students")
   
   rows = curr.fetchall(); 
   return render_template("list_students.html", rows = rows)
   
   
            
@app.route("/student/update")  
def update_student():  
    return render_template("update.html") 
    
    
@app.route("/student/change", methods = ["POST"])  
def change_student():  
    id = request.form["id"]
    email = request.form["email"]  
    with sqlite3.connect("student.db") as conn:  
        try:  
            curr = conn.cursor() 
            curr.execute("UPDATE students SET email = ? WHERE id = ?", (email, id))  
            status = "Student email changed to "+email
        except: 
            status = "Problem Updating Student email"  
        finally:  
            return render_template("update_msg.html", status = status) 
            
            
   

@app.route("/student/delete")  
def delete_student():  
    return render_template("delete.html") 
    
    
@app.route("/student/remove", methods = ["POST"])  
def remove_student():  
    id = request.form["id"]  
    with sqlite3.connect("student.db") as conn:  
        try:  
            curr = conn.cursor()  
            curr.execute("DELETE FROM students WHERE id = ?", id)  
            status = "Student "+str(id)+" Deleted!"  
        except:  
            status = "Problem Deleting Student"  
        finally:  
            return render_template("delete_msg.html", status = status) 
            

   
    
if __name__ == "__main__":  
    app.run(debug = True) 
