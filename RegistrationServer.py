from bottle import request, run, Bottle, response, template
import json
import redis
from cryptography.fernet import Fernet
key=""
redisHost="tc.inf1b.tk"
redisUsername=""
redisPassword=""
redisClient = redis.Redis(host=redisHost,port=40434,db=0,decode_responses=True,username=redisUsername,password=redisPassword)
app=Bottle()
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
        positive={"positive":"Zarejestrowano pomyślnie :)<br> Miłego logowania ;)","error":""}
        return template('login.tpl',positive)
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
@app.route('/app', method='POST')
def do_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    goodPassword=redisClient.get(username)
    if goodPassword!=None:
        goodPassword=Fernet(key).decrypt(redisClient.get(username).encode()).decode()
    if goodPassword==password:
        response.body="Zalogowano pomyślnie pomyślnie :)"
        return response
    elif goodPassword!=password or goodPassword==None:
        error={"error":"Niepoprawny login lub hasło!","positive":""}
        return template('login.tpl',error)
#fronted logowania
@app.route('/app', method='GET')
def do_login_site():
    error={"error":"","positive":""}
    return template('login.tpl',error)






run(app, host='localhost', port=8080, debug=True)