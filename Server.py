from bottle import request, run, Bottle, response, template, SimpleTemplate, redirect
import json
import redis
from cryptography.fernet import Fernet
import io
from urllib.parse import parse_qs
import sqlite3

redisClient = redis.Redis(host=redisHost,port=40434,db=0,decode_responses=True,username=redisUsername,password=redisPassword)
app=Bottle()
conn = sqlite3.connect('baza.sqlite')
c = conn.cursor()
for row in c.execute("""SELECT id FROM messages ORDER BY id DESC LIMIT 1"""):
    version=row[0]
#Backend rejestracji
@app.route('/register', method='POST')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    confirmPassword=request.forms.get('confirm_password')
    czyIsnieje=redisClient.get(username)
    if czyIsnieje==None and password==confirmPassword:
        redisClient.set(name=username,value=Fernet(key).encrypt(password.encode()).decode())
        redirect('/login?fresh=True')
    elif czyIsnieje!=None:
        error={"error":"Użytkownik o takim nicku jest już zarejestrowany."}
        return template('register.tpl',error)
    elif password!=confirmPassword:
        error={"error":"Hasła się nie zgadzają :("}
        return template('register.tpl',error)
#Frontend rejestracji
@app.route('/register', method='GET')
def do_register_site():
    error={"error":""}
    return template('register.tpl',error)
#backend logowania
@app.route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    goodPassword=redisClient.get(username)
    passwordHash=goodPassword
    if goodPassword!=None:
        goodPassword=Fernet(key).decrypt(redisClient.get(username).encode()).decode()
    if goodPassword==password:
        goodPassword=""
        response.set_cookie("username",username)
        response.set_cookie("passwordHash",passwordHash)
        response.set_cookie("id",str(version))
        response.set_cookie("reload",'true')
        redirect('/app')
    elif goodPassword!=password or goodPassword==None:
        goodPassword=""
        error={"error":"Niepoprawny login lub hasło!","positive":""}
        return template('login.tpl',error)
#fronted logowania
@app.route('/login', method='GET')
def do_login_site():
    try:
        fresh=request.query["fresh"]
    except:
        fresh="False"
    if fresh=="True":
        error={"error":"","positive":"Zarejestrowano pomyślnie :) \n Miłego logowania ;) \n"}
        return template("login.tpl",error)
    elif fresh=="False":
        error={"error":"","positive":""}
        return template("login.tpl",error)
@app.route('/app', method='GET')
def app_site():
    username = request.get_cookie("username")
    passwordHash = request.get_cookie("passwordHash")
    if username is None or passwordHash is None:
        redirect("/login")
    correctHash=redisClient.get(username)
    if correctHash!=passwordHash:
        redirect("/login")
    return template('app.tpl')
#wysyłanie wiadomości :)
@app.route('/api',"PUT")
def app_api():
    global version
    post = request.json
    username = post.get("username")
    passwordHash = post.get("passwordHash")
    message = post.get("message")
    correctHash=redisClient.get(username)
    if passwordHash==correctHash:
        tpl = SimpleTemplate('{{message}}')
        userTpl = SimpleTemplate('{{username}}')
        message=tpl.render(message=message)
        username=userTpl.render(username=username)
        c.execute(f"""INSERT INTO messages VALUES (Null,'{username}','{message}')""")
        conn.commit()
        version+=1
#odświeżanie wiadomości
@app.route('/api',"PATCH")
def seeMessages():
    try:
        username=request.json.get("username")
        passwordHash=request.json.get("passwordHash")
        lastId=int(request.json.get("lastId"))
    except:
        response.content_type = 'application/json'
        return {"messages":"Nie zalogowano / Sesja wygasła."}
    correctHash = redisClient.get(username)
    if correctHash==passwordHash:
        messages=""
        for messageBox in c.execute(f"""SELECT nickname,message FROM messages WHERE id>={lastId} ORDER BY id"""):
            messages+="""<span style="color: #79b6c9;">&lt;"""+messageBox[0]+"&gt;</span> "+messageBox[1]+"<br>"
        response.content_type = 'application/json'
        return {"messages":messages}
    else:
        response.content_type = 'application/json'
        return {"messages":"Nie zalogowano / Sesja wygasła."}
#sprawdzanie czy potrzeba odświeżać :)
@app.route('/api',"POST")
def checkFreshMessages():
    post = request.forms
    userVersion=int(post.get("id"))
    if userVersion!=version:
        response.content_type = 'application/json'
        print(version)
        return {"id":str(version),"reload":"true"}
    else:
        response.content_type = 'application/json'
        return {"id":str(userVersion),"reload":"false"}
@app.route('/',"GET")
def routeToApp():
    redirect('/app')
@app.route('/views/script.js')
def giveScript():
    file=open('views/script.js')
    content=file.read()
    file.close()
    return content
run(app, host='localhost', port=8080,reloader=True)