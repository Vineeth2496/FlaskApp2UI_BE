from flask import Flask,render_template,request, session
#pip install flask_mysqldb (mysql connector)
from flask_mysqldb import MySQL
import MySQLdb.cursors

app=Flask(__name__)

#MySQL DB Configuration
app.secret_key="d4b10"
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="vine96"
app.config["MYSQL_DB"]="db4b10"

mysql=MySQL(app)

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    message=""
    if (request.method=="POST"
            and "uid" in request.form
            and "pass" in request.form
    ):
        UserId=request.form["uid"]
        Password = request.form["pass"]

        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cur.execute("SELECT * FROM student WHERE UserId=%s and Password=%s", (UserId, Password))

        user=cur.fetchone()

        if user:
            session["LoggedIn"]=True
            session["UserId"]=user["UserId"]
            session["Password"] = user["Password"]
            session["FullName"] = user["FullName"]
            session["Email"] = user["Email"]
            message="Successfully Logged In"
            return render_template("Dashboard.html", msg=message)
        else:
            message="Please Enter Valid UserId/Password"
            return render_template("Login.html", msg=message)
    return render_template("Login.html", msg=message)
@app.route("/logout")
def logout():
    session.pop("LoggedIn", False)
    session.pop("UserId", False)
    session.pop("Password", False)
    session.pop("FullName", False)
    session.pop("Email", False)
    message="Sucessfully Logged Out"
    return render_template("Login.html", msg=message)



@app.route("/dashboard")
def dashboard():
    return render_template("Dashboard.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    message=""
    if (request.method=="POST"
            and "uid" in request.form
            and "pass" in request.form
            and "name" in request.form
            and "email" in request.form
            and "phno" in request.form
            and "gn" in request.form
        ):
        UserId = request.form["uid"]
        Password = request.form["pass"]
        FullName=request.form["name"]
        Email = request.form["email"]
        PhoneNo = request.form["phno"]
        Gender = request.form["gn"]

        cur=mysql.connection.cursor()   #MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s)",(UserId, Password, FullName, Email, PhoneNo, Gender))
        mysql.connection.commit();
        message="Successfully Account is Created"
        return render_template("Login.html", msg=message)
    else:
        # flash("Please SignUp", "/register")
        message="Please fill the form"

    return render_template("Register.html", msg=message)



# @app.route("/insert", methods=["POST", "GET"])
# def insert():
#     if request.method=="POST":
#         Name=request.form["name"]
#         Email = request.form["email"]
#         Password = request.form["pass"]
#         PhoneNo = request.form["phno"]
#         Gender = request.form["gn"]
#
#         return f"Name : {Name}, Email: {Email}, Password: {Password}, PhoneNo:{PhoneNo}, Gender:{Gender}"
#     else:
#         # flash("Please SignUp", "/register")
#         return redirect(url_for("register"))

if __name__=="__main__":
    app.run(debug=True)