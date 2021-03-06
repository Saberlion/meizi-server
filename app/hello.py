import json

from flask import Flask, jsonify

from db import Meizi, DB_ADD

app = Flask(__name__)
#app.config.from_pyfile('hello.cfg')

class res:
    code =''
    msg= ''
    res =[]
    def __init__(self, code, msg, res):
        self.code = code
        self.msg = msg
        self.res = res

@app.route('/')
def hello():
    return "hello"

@app.route('/api/meizi/<int:num>/random',methods=['GET'])
def getRandomMeizi(num):
    randomMeizi = Meizi.getRandomN(num)

    meizis = []
    for item in randomMeizi:
        meizis.append({'filename':item.filename})

    res = {}
    res['code']=0
    res['msg']='success'
    res['meizi']=meizis
    return json.dumps(res)

@app.route('/api/meizi/<filename>/upload',methods=['GET'])
def meizi_upload(filename):
    DB_ADD(Meizi(filename))
    return jsonify(
        {
        "code":0,
        "msg":'success',
        "meizi":filename
        }
    )

if __name__ == '__main__':
    app.run(debug=True)