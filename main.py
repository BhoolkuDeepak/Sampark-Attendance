from flask import Flask, render_template, request, session
app = Flask(__name__)

#MODEL
class user :
    def __init__(self,username,first_name,last_name,password,email,age,country,city):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.country= country
        self.city= city
        
    
#Repository
class UserRepository :
    def check_user(new_user):
        import mysql.connector
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Deepak1002",
            database="Sampark"
            )
        cursor = mydb.cursor()
        cursor.execute('''SELECT username FROM users where username = %s ''',[new_user.username])
        output=cursor.fetchall()
        print(output)
        print(len(output))
        if len(output) == 0 :
            cursor.execute(''' INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
                           (new_user.username,new_user.first_name,new_user.last_name,
                            new_user.password,new_user.email,new_user.age,new_user.country,
                            new_user.city))
            print("Added")
            mydb.commit()
            cursor.close()
            return True
        else :
            mydb.commit()
            cursor.close()
            return False
    
    def login_check(username,password):
        import mysql.connector
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Deepak1002",
            database="Sampark"
            )
        cursor = mydb.cursor()
        cursor.execute('''SELECT username FROM users where username = %s ''',[username])
        username_output=cursor.fetchall()
        if username_output==None:
            return None
        else:
            cursor.execute('''SELECT username FROM users where username = %s and passcode = %s''',
                           [username,password])
            password_output=cursor.fetchall
            if password_output==None:
                return False
            else:
                return True
    
#SERVICE
class UserService :
    def signup(data):
        username=data.get("username")
        first_name=data.get("first_name")
        last_name=data.get("last_name")
        password=data.get("password")
        email=data.get("email")
        age=data.get("age")
        country=data.get("country")
        city=data.get("city")
        new_user=(user(username,first_name,last_name,password,email,age,country,city))
        approval=UserRepository.check_user(new_user)
        if approval==False:
            return False
        elif approval==True:
            return True
        
    def login(data):
        username=data.get("username")
        password=data.get("password")
        approval=UserRepository.login_check(username,password)
        if approval == None:
            return None
        elif approval == False:
            return False
        else:
            return True
        
        
#HOME PAGE
@app.route("/")
def home_page():
    return render_template("home.html")

#SIGNUP PAGE [GET]
@app.route("/signup",methods=["GET"])
def get_user_data():
    return render_template("signup.html")

#SIGNUP PAGE [POST]
@app.route("/signup",methods=["POST"])   
def signup():
    new_user=UserService.signup(request.form)
    if new_user==True:
        print("New User")
        return render_template("home.html")
    else:
        print("User Exits")
        return render_template("signup.html",error=True)
    
#LOGIN PAGE [GET]
@app.route("/login")
def get_login_info():
    return render_template("login.html")

#LOGIN PAGE [POST]
@app.route("/login",methods=["POST"])
def authenicate_data():
    user=UserService.login(request.form)
    if user==None:
        return render_template ("login.html",error="True")
    elif user==False:
        return render_template ("login.html",errors="True")
    else:
        return render_template ("success.html")

app.run(debug=True,port=8085)