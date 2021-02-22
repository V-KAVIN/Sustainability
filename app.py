from flask import Flask,redirect,render_template,request,url_for
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from sqlalchemy import text
import requests

app=Flask(__name__)

app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="**********",
    password="**********",
    hostname="**********",
    databasename="**********",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

USER_DATA={
    "name":"**********","password":"**********"
}

def execute(query):
   t=text(query)
   result=db.session.execute(t)
   res=result.fetchall()
   return res

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/mob')
def mobindex():
    return render_template('moblogin.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form["name"]
        pwd=request.form["pwd"]
        if name.lower()==USER_DATA["name"].lower() and pwd==USER_DATA["password"]:
            return redirect(url_for('details'), code=307)
        return redirect('/')
    return redirect('/')

@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method=='POST':
        name=request.form["name"]
        pwd=request.form["pass"]
        na='SELECT password from '+name
        try:
            na=execute(na)
        except:
            return render_template("notfound.html",msg="OOPS! USER DOES NOT EXISTS")
        newpwd=str(na[0][0])
        if pwd==newpwd:
            return redirect(url_for('health'), code=307)
        return render_template("notfound.html",msg="Incorrect Password")
    return redirect('/')

@app.route('/details',methods=['GET','POST'])
def details():
    if request.method=="POST":
        a=execute('show tables')
        res=[]
        for i in a:
            te=str(i)
            res.append(te[2:-3])
        c=0
        ite=[]
        for i in res:
            c+=1
            fn='SELECT fname FROM '+i
            ln='SELECT lname FROM '+i
            jo='SELECT job FROM '+i
            fn=execute(fn)
            ln=execute(ln)
            jo=execute(jo)
            fn1,ln1,jo1=[],[],[]
            for k in range(len(fn)):
                for j in fn[k].values():
                    fn1.append(j)
                for j in ln[k].values():
                    ln1.append(j)
                for j in jo[k].values():
                    jo1.append(j)
            temp=[c,fn1,ln1,jo1,i]
            ite.append(temp)
        return render_template('result.html',ite=ite,n=len(ite))
    return redirect('/')

@app.route('/sdetails',methods=['GET','POST'])
def sdetails():
    if request.method=="POST":
        name=request.form["name"]
        res='SELECT * FROM '+name
        res=execute(res)
        det=[res[0][0]+' '+res[0][1],res[0][2],res[0][3],res[0][4],res[0][5],res[0][6]]
        URL = "http://blynk-cloud.com/**********/get/V8"
        URL1 ="http://blynk-cloud.com/**********/get/V7"
        r = requests.get(URL)
        r1= requests.get(URL1)
        soup = BeautifulSoup(r.content, 'html5lib')
        soup1 = BeautifulSoup(r1.content, 'html5lib')

        BPM=soup.find('body').getText()
        Spo2=soup1.find('body').getText()

        bpm=BPM[2:-2]
        spo2=Spo2[2:-2]

        return render_template('details.html',det=det,bpm=bpm,spo2=spo2)
    return redirect('/')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        uname=request.form["uname"]
        fname=request.form["fname"]
        lname=request.form["lname"]
        age=request.form["age"]
        gender=request.form["gender"]
        height=request.form["height"]
        wei=request.form["weight"]
        job=request.form["job"]
        phone=request.form["phone"]
        email=request.form["email"]
        password=request.form["password"]
        try:
            query="CREATE TABLE "+uname+" (fname VARCHAR(50),lname VARCHAR(50),age VARCHAR(3),gender VARCHAR(10),height VARCHAR(5),weight VARCHAR(5),job VARCHAR(50),phone VARCHAR(15),beat VARCHAR(15),spo2 VARCHAR(15),time VARCHAR(50),email VARCHAR(30),password VARCHAR(30))"
            table=text(query)
            db.session.execute(table)
            db.session.commit()
        except:
            return render_template("notfound.html",msg="User Name Already Exists !")
        table=text("INSERT INTO "+uname+" (fname,lname,age,gender,height,weight,job,phone,email,password) VALUES(:fname,:lname,:age,:gender,:height,:weight,:job,:phone,:email,:password)")\
        .bindparams(fname=fname,lname=lname,age=age,gender=gender,height=height,weight=wei,job=job,phone=phone,email=email,password=password)
        db.session.execute(table)
        db.session.commit()
        return render_template("notfound.html",msg="Registration Successful !")
    return redirect('/')

@app.route('/health',methods=['GET','POST'])
def health():
    return render_template('mobdetail.html')

@app.route('/reg')
def reg():
    return render_template('register.html')

@app.route('/test')
def test():
    req = urllib.request.Request("http://blynk-cloud.com/**********/get/V8")
    try:
        urllib.request.urlopen(req).read()
        return "success"
    except urllib.error.HTTPError as e:
        return "Error: "+str(e.code)

if __name__ == '__main__':
    app.run(debug=True)