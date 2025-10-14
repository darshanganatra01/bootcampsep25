from flask import Flask,render_template,request,redirect,session,flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy #importing


app = Flask(__name__)


#URI -- Uniform resource identifier
app.config['SECRET_KEY']='saltandpepper'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bootcamp.db' #configuration


db = SQLAlchemy()  #initialization
db.init_app(app)  #integration

migrate = Migrate(app,db)  #integration of migrate with app and db

#if this happens 
#you will do this 


app.app_context().push()


#use

class Role(db.Model):
    rid = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(100),unique=True,nullable=False)
    description = db.Column(db.String(200),nullable=True)

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    f_rid = db.Column(db.Integer,db.ForeignKey(Role.rid),nullable=True)



db.create_all()  #creates the database TABLES


#1. if user wants to login first you will
# give them a login page

#when user submits the data u need to verify the password 
# u need to check if the uer is inside the database

#when user comes for the first time say hii 

#taskkss to execute ---> Functions 

@app.route("/")   #only get method
def hii():
    return render_template("landing.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        #read the sended data
        form_email = request.form["email"]
        form_password = request.form["password"]
        print(form_email,form_password)
        #First i am going to check that the user with that email ex
        #exists or not 
        #filter
        check_user = User.query.filter_by(email=form_email,f_rid=1).first() #None
        print(check_user) #None
        #this below thing will work only if user exitst
        
        if check_user:
            if check_user.password == form_password:
                print("password is correct dshn=board came")
                session['email'] = check_user.email
                return redirect('/dashboard')    #Dashboard
            #redirect to appointments
            else:
                print("Password is incorrect went to login")
                flash("Password is incorrect")
                return redirect('/login')  #LOGIN
        else:
            print("User Not Found went to signup")
            return redirect('/signup')  #SIGNUP
        

@app.route("/admin_login",methods=['GET','POST'])
def admin_login():
    if request.method=="GET":
        return render_template("admin_login.html")
    else:
        form_email = request.form["email"]
        form_password = request.form["password"]

        #Credentials are matching admin credentials or not 
        # f_rid == 2 
        # email == admin@gmail.com
        check_admin= User.query.filter_by(email=form_email,f_rid=2).first()
        if check_admin:
            if check_admin.password == form_password:
                session['email'] = check_admin.email
                return redirect('/admin_dashboard')    #Dashboard
            else:
                flash("Password is incorrect")
                return redirect('/admin_login')  #LOGIN
        else:
            flash("Admin User Not Found, contact support")
            return redirect('/admin_login')  #LOGIN

@app.route("/admin_dashboard")
def admin_dashboard():
    email = session.get('email')
    return render_template("admin_dashboard.html",jinjaemail=email)

@app.route("/theatre_login",methods=['GET','POST'])
def theatre_login():
    if request.method=="GET":
        return render_template("theatre_login.html")
    else:
        form_email = request.form["email"]
        form_password = request.form["password"]

        check_theatre= User.query.filter_by(email=form_email,f_rid=3).first()

        if check_theatre:
            if check_theatre.password == form_password:
                session['email'] = check_theatre.email
                return redirect('/theatre_dashboard')    #Dashboard
            else:
                flash("Password is incorrect")
                return redirect('/theatre_login')  #LOGIN
        else:
            flash("Theatre User Not Found, contact support")
            return redirect('/theatre_login')  #LOGIN

@app.route("/theatre_dashboard")
def theatre_dashboard():
    email = session.get('email')
    return render_template("theatre_dashboard.html",jinjaemail=email)


@app.route("/signup",methods=['GET','POST'])
def signup():
    if request.method=="GET":
        return render_template("signup.html")
    else:
        form_email = request.form["email"]
        form_password = request.form["password"]
        #check if the user with that email already exists
        check_user = User.query.filter_by(email=form_email,f_rid=1).first()
        #all()
        if check_user:
            flash("User already exists, please login")
            return redirect('/login')
        else:
            #create a new user
            new_user = User(email=form_email,password=form_password,f_rid=1)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')


#CRUD
#Create Read Update Delete

#that send the data to the server from html
#but first make server ready to accept the data

#/dashboard/n
#login
#signup
#dashboard


@app.route("/dashboard/") 
def dashboard():
    email = session.get('email')
    return render_template("dashboard.html",jinjaemail=email)




def create_roles():
    check_userrole = Role.query.filter_by(rolename="User").first()
    if not check_userrole:
        user_role = Role(rolename="User",description="Can book appointments")
        db.session.add(user_role)
        db.session.commit()
    check_adminrole = Role.query.filter_by(rolename="Admin").first()
    if not check_adminrole:
        admin_role = Role(rolename="Admin",description="Can manage the website")
        db.session.add(admin_role)
        db.session.commit()
    check_theatrerole = Role.query.filter_by(rolename="Theatre").first()
    if not check_theatrerole:
        theatre_role = Role(rolename="Theatre",description="Can manage the Bookings")
        db.session.add(theatre_role)
        db.session.commit()
    
def check_admin():
    check_admin = User.query.filter_by(f_rid=2).first()
    if not check_admin:
        admin_user = User(email="admin@gmail.com",password="admin123",f_rid=2)
        db.session.add(admin_user)
        db.session.commit()


if __name__ == "__main__":
    create_roles()
    check_admin()
    app.run(debug=True)
#fvgfngh




