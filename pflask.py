from flask import Flask,request, Response, render_template
import uuid
import time
from flask_cors import CORS
import json

app = Flask(__name__,static_url_path='/static')

CORS(app)

app = Flask(__name__)

users = {}
msg = []
name = ""
text = ""


@app.route("/")
def main():
    return render_template ('index.html')

@app.route('/auth')
def authh():
    name = request.args.get('name')
    if name not in users:
        token = str(uuid.uuid4())
        users[name] = token
        return Response(token, status = 200, mimetype = "text/plain")
    elif name == None:
        return Response("Не указали имя",status = 400, mimetype = "text/plain")
    else:
        return Response("Такой пользователь уже есть",status = 403, mimetype = "text/plain")

@app.route('/users')
def userss():
    return (f'{users}')

@app.route('/send')
def sendd():
    text = request.args.get('text')
    token = request.args.get('token')
    count = 0
    for i in token:
        count += 1
    name = None
    for key,value in users.items():
            if value == token:
                name =  key

    if text == None:
        return Response('Не указан текст',status = 400)
    if token == None:
        return Response("Не указан токен",status = 400)
    if count != 36:
        return Response("Неправильный токен",status = 400)
    name = None
    for key,value in users.items():
        if value == token:
            name = key
    if name != None:
        timestamp = time.time()
        msg.append({'name': name,
                    'text': text,
                    'time': timestamp})
        return Response("Сообщение отправлено", status = 200, mimetype = "text/plain")
    else:
        return Response("Пустое имя",status = 403, mimetype = "text/plain")
    
@app.route("/logout")
def logoutt():
    tokn = request.args.get('token')
    if tokn == None:
        return Response("Не указан токен",status = 400, mimetype = "text/plain")
    else:
        for key,value in users.items():
            if value == tokn:
                del users[key]
                return Response("Вы успешно вышли из системы", status = 200, mimetype = "text/plain")
        return Response("Не найден токен",status = 403, mimetype = "text/plain")
        
@app.route('/getall')
def getalll():
    token = request.args.get('token')
    for j in users.items():
        if j == token:
            return Response(json.dumps(msg), status = 200)
    return Response("Токен не найден",status = 403)

if __name__ == '__main__':
    app.run(debug=True)