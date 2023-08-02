from bottle import request, run, Bottle, response
import json
import redis
redisHost="tc.inf1b.tk"
redisUsername="default"
redisPassword="RGErGUXwwVX76TUh458dirUMVyV"
redisClient = redis.Redis(host=redisHost,port=40434,db=0,decode_responses=True,username=redisUsername,password=redisPassword)
app=Bottle()
@app.route('/register', method='POST')
def do_login():
    username = request.forms.get('username')
    password="+"
    password += request.forms.get('password')
    czyIsnieje=redisClient.acl_getuser(username)
    if czyIsnieje==None:
        redisClient.acl_setuser(username=username, enabled=True, nopass=False, passwords=password, hashed_passwords=None,  commands=["+get","+set"], categories=None, keys="*", channels="*", selectors=None, reset=False, reset_keys=False, reset_channels=False, reset_passwords=False)
        response.body="Zarejestrowano pomyślnie :)"
        return response
    else:
        response.body="Użytkownik o takim nicku już jest zarejestrowany."
        return response
@app.route('/register', method='GET')
def do_login():
    return """Aby się zarejestować skorzystaj z formularza: <br><form action="/register" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Zarejestruj" type="submit" />
        </form>"""
run(app, host='localhost', port=8080, debug=True)