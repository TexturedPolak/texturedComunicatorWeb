from bottle import request, run, Bottle, response, template, SimpleTemplate, redirect
import json
import redis
from cryptography.fernet import Fernet
import io

redisClient = redis.Redis(host=redisHost,port=40434,db=0,decode_responses=True,username=redisUsername,password=redisPassword)
app=Bottle()
version=0
#Backend rejestracji
@app.route('/register', method='POST')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    confirmPassword=request.forms.get('confirm_password')
    czyIsnieje=redisClient.acl_getuser(username)
    if czyIsnieje==None and password==confirmPassword:
        redisClient.acl_setuser(username=username, enabled=True, nopass=False, passwords="+"+password, hashed_passwords=None,  commands=["+get","+set"], categories=None, keys="*", channels="*", selectors=None, reset=False, reset_keys=False, reset_channels=False, reset_passwords=False)
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
        response.set_cookie("username",username)
        response.set_cookie("passwordHash",passwordHash)
        response.set_cookie("LocalVersion",str(version))
        response.set_cookie("reload",'true')
        redirect('/app')
    elif goodPassword!=password or goodPassword==None:
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
@app.route('/api',"POST")
def app_api():
    global version
    post = request.json
    username = post.get("username")
    passwordHash = post.get("passwordHash")
    message = post.get("message")
    correctHash=redisClient.get(username)
    if passwordHash==correctHash:
        message=f"<{username}> {message}"
        tpl = SimpleTemplate('{{message}}')
        message=tpl.render(message=message)
        file=open('views/messages.tpl','a')
        file.write(f"{message}<br>\n")
        file.close()
        version+=1
#odświeżanie wiadomości
@app.route('/messages',"GET")
def seeMessages():
    return template('messages.tpl')
#sprawdzanie czy potrzeba odświeżać :)
@app.route('/api/messages',"POST")
def checkFreshMessages():
    global version
    post = request.forms
    userVersion=int(post.get("LocalVersion"))
    if userVersion!=version:
        response.content_type = 'application/json'
        return {"LocalVersion":str(version),"reload":"true"}
    else:
        response.content_type = 'application/json'
        return {"LocalVersion":str(userVersion),"reload":"false"}
run(app, host='localhost', port=8080, debug=True, reloader=True)