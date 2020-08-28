from flask import Flask,render_template,request,session
from flask import *
import speech_recognition as sr
from werkzeug.utils import secure_filename
import mysql.connector
import webbrowser as wb
import hashlib, os
from datetime import date as date5



d={"redmi note 7":["xiaomi_redmi_note_7-9513.php",9999],"samsung galaxy a71":["samsung_galaxy_a71-9995.php",29999],"vivo s1":["vivo_s1-9766.php",15999],
   "redmi note 4":["xiaomi_redmi_note_4-8531.php",12990],"samsung galaxy a60":["samsung_galaxy_a60-9616.php",22176],"vivo y12":["vivo_y12-9729.php",10450],
   "redmi note 8":["xiaomi_redmi_note_8-9814.php",10499],"samsung galaxy s10":["samsung_galaxy_s10-9536.php",54900],"vivo v17":["vivo_v17_(india)-9982.php",21500],
   "redmi note 6 pro":["xiaomi_redmi_note_6_pro-9333.php",10999],"samsung galaxy a70":["samsung_galaxy_a70-9646.php",18999],"vivo s5":["vivo_s5-9948.php",16280],
   "redmi note 5 pro":["xiaomi_redmi_note_5_pro-8893.php",13999],"samsung galaxy a30":["samsung_galaxy_a30-9579.php",13999],"vivo y3":["vivo_y3_(4gb+64gb)-9951.php",12999],
   "redmi 8":["xiaomi_redmi_8-9800.php",8999],"samsung galaxy a7":["samsung_galaxy_a7_(2018)-9340.php",14999],"vivo z5":["vivo_z5-9782.php",15999]
   }


def sql_connection(d_name,t_name,host='localhost',user='root',password='password'):
    try:
        mydb=mysql.connector.connect(host=host,user=user,password=password)
        cur=mydb.cursor()
        try:
            cur.execute(f"create database {d_name}")
        except:
            pass
        mydb=mysql.connector.connect(host='localhost',user='root',password='password',database=d_name)
        cur=mydb.cursor()
        try:
            s=f'''create table {t_name}(password varchar(100),productname varchar(100),price Integer,date varchar(100),quantity varchar(100),color varchar(100),email varchar(100)
            , fullName varchar(100),address1 varchar(100), address2 varchar(100), zipcode varchar(100), city varchar(100), state varchar(100), country varchar(100),
            contact varchar(100))'''
            cur.execute(s)
            cur.execute('''CREATE TABLE users (userId INTEGER PRIMARY KEY AUTO_INCREMENT, password TEXT,email TEXT,firstName TEXT,address1 TEXT,address2 TEXT,
                zipcode TEXT,city TEXT,state TEXT,country TEXT, phone TEXT)''')
            
        except Exception as e:
            print(e)
            
            pass
    except Exception as e:
        print(e)
sql_connection(d_name="bussiness4",t_name="order_data")
app=Flask(__name__)
app.secret_key = 'random string'

fullname=""
email=""
address1=""
address2=""
contact=""
zipcode=""
city=""
state=""
country=""
password=""
productname=""
price=""
date=""
quantity=""
color=""

def text():
    while True:
        with sr.Microphone() as source:
            print("speak now")
            r=sr.Recognizer()
            audio=r.listen(source)
            try:
                a=r.recognize_google(audio)
                print(a)
            except Exception as e:
                print("Say it again")
                print(e)
            else:
                break
    return a
@app.route("/target",methods=["POST"])
def target():
    if request.method=="POST":
        r=text()
        r=r.lower()
        page=r.split(" ")[0]
        if "specification" in r:
            for i in d.keys():
                url="https://www.gsmarena.com/"
                if i in r:
                    try:
                        wb.get().open_new(url+d[i][0])
                    except sr.UnknownValueError:
                        print("error")
                    except sr.RequestError as e:
                        print("failed".format(e))
                    except:
                        return redirect(url_for('index'))
            return render_template(f"{page}.html")
        elif "redmi" in r:
            return render_template("redmi.html")
        elif "samsung" in r:
            return render_template("samsung.html")
        elif "vivo" in r:
            return render_template("vivo.html")
        elif "order" in r:
            if 'email' not in session:
                return render_template("login.html")
            else:
                return render_template("app.html")
        elif ("login" in r) or ("sign in" in r):
            return render_template("login.html")
        elif ("sign up" in r) or ("signup" in r) or ('register' in r):
            return render_template("register.html")
        else:
            return redirect(url_for('index'))
    
def is_valid(email, password):
    con=mysql.connector.connect(host='localhost',user='root',password='password',database="bussiness4")
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    print(data)
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('index'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)
def getLoginDetails():
        conn=mysql.connector.connect(host='localhost',user='root',password='password',database="bussiness4")
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = '" + session['email'] + "'")
            userId, firstName = cur.fetchone()
        conn.close()
        return (loggedIn, firstName)
@app.route("/")
def root():
    loggedIn, firstName= getLoginDetails()  
    return render_template('index.html',loggedIn=loggedIn,firstName=firstName.split(" ")[0])

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(password)
        con=mysql.connector.connect(host='localhost',user='root',password='password',database="bussiness4")
        try:
            cur = con.cursor()
            cur.execute('INSERT INTO users (password, email, firstName,address1, address2, zipcode, city, state, country, phone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (hashlib.md5(password.encode()).hexdigest(), email, fullname,address1, address2, zipcode, city, state, country, contact))
            con.commit()
            msg = "Registered Successfully"
        except Exception as e:
            print(e)
##            con.rollback()
            msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)
@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))



@app.route("/productname",methods=["POST"])
def productname1():
    if request.method=="POST":
        a=text()
        global productname
        global price
        global date
        productname=a
        date=date5.today()
        try:
            price=d[a.lower()][1]
        except:
            pass
        return render_template("app.html",productname=productname,price=price,date=date,quantity=quantity,color=color)
    return "not worked productname"

@app.route("/quantity",methods=["POST"])
def quantity1():
    if request.method=="POST":
        b=text()
        global quantity
        quantity=b
        return render_template("app.html",productname=productname,price=price,date=date,quantity=quantity,color=color)
    return "not worked quantity"

##@app.route("/date",methods=["POST"])
##def date1():
##    if request.method=="POST":
##        c=text()
##        global date
##        date=c
##        return render_template("app.html",price=price,productname=productname,quantity=quantity,date=date,contact=contact,fullname=fullname,color=color,email=email,address=address)
##    return "not worked date"

@app.route("/password",methods=["POST"])
def password1():
    if request.method=="POST":
        a = request.form.get('password')
        print(a)
        global password
        password=a
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked password"


@app.route("/fullname",methods=["POST"])
def name1():
    if request.method=="POST":
        d=text()
        global fullname
        fullname=d
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked name"
@app.route("/color",methods=["POST"])
def color1():
    if request.method=="POST":
        d=text()
        global color
        color=d
        return render_template("app.html",productname=productname,price=price,date=date,quantity=quantity,color=color)
    return "not worked color"
@app.route("/email",methods=["POST"])
def email1():
    if request.method=="POST":
        d=text()
        global email
        email=d.lower().replace(" ","")
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked email"
@app.route("/address1",methods=["POST"])
def address3():
    if request.method=="POST":
        d=text()
        global address1
        address1=d
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked address1"
@app.route("/address2",methods=["POST"])
def address4():
    if request.method=="POST":
        d=text()
        global address2
        address2=d
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked address2"
@app.route("/contact",methods=["POST"])
def contact1():
    if request.method=="POST":
        d=text()
        global contact
        contact=d.lower().replace(" ","")
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked contact"
@app.route("/zipcode",methods=["POST"])
def zipcode1():
    if request.method=="POST":
        d=text()
        global zipcode
        zipcode=d
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked zipcode"
@app.route("/city",methods=["POST"])
def city1():
    if request.method=="POST":
        d=text()
        global city
        city=d
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked city"
@app.route("/state",methods=["POST"])
def state1():
    if request.method=="POST":
        d=text()
        global state
        state=d
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked stste"

@app.route("/country",methods=["POST"])
def country1():
    if request.method=="POST":
        d=text()
        global country
        country=d
        return render_template("register.html",password=password,contact=contact,fullname=fullname,email=email,address1=address1,address2=address2,zipcode=zipcode,city=city,state=state,country=country)
    return "not worked country"
@app.route("/final",methods=["POST"])
def final():
    global productname
    global quantity
    global color
    global date
    global price
    global contact
    global fullname
    global email
    global address1
    global address2
    global zipcode
    global city
    global state
    global country
    global password
    print(date)
    conn=mysql.connector.connect(host='localhost',user='root',password='password',database="bussiness4")
    cur = conn.cursor()
    search=session['email']
    u=None
    cur.execute(f'SELECT userid ,email FROM users')
    data = cur.fetchall()
    print(data)
    for i in data:
        if search==i[1]:
            u=i[0]
    cur.execute(f'SELECT * FROM users where userId={u}')
    data = cur.fetchall()
            
        
    u_id,password, email, fullName,address1, address2, zipcode, city, state, country, contact=data[0]
    mydb=mysql.connector.connect(host='localhost',user='root',password='password',database='bussiness4')
    s="insert into order_data(password,productname,price,date,quantity,color,email, fullName,address1, address2, zipcode, city, state, country, contact) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    t=(password,productname,price,date,quantity,color,email, fullName,address1, address2, zipcode, city, state, country, contact)
    print(t)
    cur=mydb.cursor()
    cur.execute(s,t)
    mydb.commit()
    v=str(t[3])
    if int(v[8:])>=25:
        v=v[:8]+'00'
    p1=t[2]*int(t[4])
    p2=133.75*int(t[4])
    password,productname,price,date,quantity,color,email, fullName,address1, address2, zipcode, city, state, country, contact="","","","","","","","","","","","","","",""
    return render_template("confirm.html",price=t[2],totalprice=(t[2]*int(t[4]))+(133.75*int(t[4]))+199,address1=t[8],address2=t[9],delivarydate=t[3],delivarydate1=v[:8]+str(int(v[8:])+4),productname=t[1],zipcode=t[10],quantity=t[4],p1=p1,p2=p2)       
    
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/redmi")
def redmi():
    return render_template("redmi.html")
@app.route("/samsung")
def samsung():
    return render_template("samsung.html")
@app.route("/vivo")
def vivo():
    return render_template("vivo.html")
@app.route("/blogd")
def blogd():
    return render_template("confirm.html")





print(app.run(debug=True))
