import bottle
import redis
import sqlite3
import json
from bottle import request, run, Bottle, response, template
from bottle import SimpleTemplate, redirect
from cryptography.fernet import Fernet


# some variables
key = ""
redisHost = ""
redisUsername = ""
redisPassword = ""


# Config all libraries
redisClient = redis.Redis(host=redisHost, port=40434, db=0,
                          decode_responses=True, username=redisUsername,
                          password=redisPassword)
# For reverse proxy
# def fix_environ_middleware(app):
#     def fixed_app(environ, start_response):
#         environ['wsgi.url_scheme'] = 'https'
#         environ['HTTP_X_FORWARDED_HOST'] = 'chat.texturedpolak.xyz'
#         return app(environ, start_response)
#     return fixed_app
# app = bottle.default_app()
# app.wsgi = fix_environ_middleware(app.wsgi)
# for none reverse proxy
app = Bottle()
conn = sqlite3.connect('baza.sqlite')
c = conn.cursor()


# Sync one variable with database
for row in c.execute("""SELECT id FROM messages ORDER BY id DESC LIMIT 1"""):
    version = row[0]


# Register backend
@app.route('/register', method='POST')
def doRegister():
    username = request.forms.get('username')
    password = request.forms.get('password')
    confirmPassword = request.forms.get('confirm_password')
    czyIsnieje = redisClient.get(username)
    if czyIsnieje is None and password == confirmPassword:
        redisClient.set(name=username,
                        value=Fernet(key).encrypt(password.encode()).decode())
        redirect('/login?fresh=True')
    elif czyIsnieje is not None:
        error = {"error": "Użytkownik o takim nicku jest już zarejestrowany."}
        return template('register.tpl', error)
    elif password != confirmPassword:
        error = {"error": "Hasła się nie zgadzają :("}
        return template('register.tpl', error)


# Register Frontend
@app.route('/register', method='GET')
def doRegisterSite():
    error = {"error": ""}
    return template('register.tpl', error)


# Login backend
@app.route('/login', method='POST')
def doLogin():
    username = request.forms.get('username')
    password = request.forms.get('password')
    goodPassword = redisClient.get(username)
    passwordHash = goodPassword
    if goodPassword is not None:
        goodPassword = Fernet(key).decrypt(redisClient.get(username)
                                           .encode()).decode()
    if goodPassword == password:
        goodPassword = ""
        response.set_cookie("username", username)
        response.set_cookie("passwordHash", passwordHash)
        response.set_cookie("id", str(version))
        response.set_cookie("reload", 'true')
        redirect('/app')
    elif goodPassword != password or goodPassword is None:
        goodPassword = ""
        error = {"error": "Niepoprawny login lub hasło!", "positive": ""}
        return template('login.tpl', error)


# Login frontend
@app.route('/login', method='GET')
def doLoginSite():
    try:
        fresh = request.query["fresh"]
    except KeyError:
        fresh = "False"
    if fresh == "True":
        error = {"error": "",
                 "positive": """Zarejestrowano pomyślnie :)
                 Miłego logowania ;) \n"""}
        return template("login.tpl", error)
    elif fresh == "False":
        error = {"error": "", "positive": ""}
        return template("login.tpl", error)


@app.route('/app', method='GET')
def appSite():
    username = request.get_cookie("username")
    passwordHash = request.get_cookie("passwordHash")
    if username is None or passwordHash is None:
        redirect("/login")
    correctHash = redisClient.get(username)
    if correctHash != passwordHash:
        redirect("/login")
    return template('app.tpl')


# Send messages :)
@app.route('/api', "PUT")
def appApi():
    global version
    post = request.json
    username = post.get("username")
    passwordHash = post.get("passwordHash")
    message = post.get("message")
    correctHash = redisClient.get(username)
    if passwordHash == correctHash:
        c.execute(f"INSERT INTO messages VALUES \
                  (Null, ?, ?)", (username, message))
        conn.commit()
        version += 1


# Refresh messages
@app.route('/api', "PATCH")
def seeMessages():
    try:
        username = request.json.get("username")
        passwordHash = request.json.get("passwordHash")
        lastId = int(request.json.get("lastId"))
        html = request.json.get("html")
    except KeyError:
        response.content_type = 'application/json'
        return {"messages": "Nie zalogowano / Sesja wygasła.",
                "lastId": version}
    correctHash = redisClient.get(username)
    if correctHash == passwordHash:
        if html:
            messages = ""
            for messageBox in c.execute(f"SELECT nickname,message FROM \
                                        messages WHERE id>? ORDER BY id",
                                        (lastId,)):
                tpl = SimpleTemplate('{{message}}')
                userTpl = SimpleTemplate('{{username}}')
                message = tpl.render(message=messageBox[1])
                username = userTpl.render(username=messageBox[0])
                messages += """<span style="color: #79b6c9;">&lt;"""\
                         + username\
                         + "&gt;</span> "\
                         + message\
                         + "<br>\n"
            response.content_type = 'application/json'
            return {"messages": messages,
                    "lastId": version}
        if html is False:
            messages = []
            for messageBox in c.execute(f"SELECT nickname,message,id FROM \
                                        messages WHERE id>? ORDER BY id",
                                        (lastId,)):
                message = messageBox[1]
                username = messageBox[0]
                id = messageBox[2]
                messages.append({"username": username,
                                 "message": message,
                                 "id": id})
            response.content_type = 'application/json'
            return {"messages": messages,
                    "lastId": version}
    else:
        response.content_type = 'application/json'
        return {"messages": "Nie zalogowano / Sesja wygasła.",
                "lastId": version}


# Check if need to reload messages
@app.route('/api', "POST")
def checkFreshMessages():
    post = request.forms
    userVersion = int(post.get("id"))
    if userVersion != version:
        response.content_type = 'application/json'
        return {"reload": "true"}
    else:
        response.content_type = 'application/json'
        return {"reload": "false"}


# Redirect to app from root domain
@app.route('/', "GET")
def routeToApp():
    redirect('/app')


@app.route('/views/script.js')
def giveScript():
    file = open('views/script.js')
    content = file.read()
    file.close()
    return content


# Run this :)
run(app, host='localhost', port=8080)
